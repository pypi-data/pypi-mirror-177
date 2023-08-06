"""
Concrete :class:`~.base.TrackerJobsBase` subclass for MTV
"""

from ... import __homepage__, __project_name__, jobs, utils
from ...utils import cached_property
from ...utils.release import ReleaseType
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class MtvTrackerJobs(TrackerJobsBase):

    torrent_piece_size_max = 8 * 2**20  # 8 MiB

    @cached_property
    def jobs_before_upload(self):
        return (
            # Background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,

            # Interactive jobs
            self.category_job,
            self.tmdb_job,
            self.tvmaze_job,
            self.title_job,
            self.description_job,
        )

    @property
    def isolated_jobs(self):
        if self.options.get('only_description', False):
            return (
                self.mediainfo_job,
                self.screenshots_job,
                self.upload_screenshots_job,
                self.description_job,
            )
        elif self.options.get('only_title', False):
            return (
                self.title_job,
                self.tmdb_job,
                self.tvmaze_job,
            )
        else:
            # Activate all jobs
            return ()

    @cached_property
    def category_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('category'),
            label='Category',
            condition=self.make_job_condition('category_job'),
            autodetect=self.autodetect_category,
            choices=[
                (c['label'], c['value'])
                for c in self._categories
            ],
            callbacks={
                'finished': self.propagate_category,
            },
            **self.common_job_args(),
        )

    _categories = (
        {'label': 'HD Season', 'value': '5', 'type': ReleaseType.season},
        {'label': 'HD Episode', 'value': '3', 'type': ReleaseType.episode},
        {'label': 'HD Movie', 'value': '1', 'type': ReleaseType.movie},
        {'label': 'SD Season', 'value': '6', 'type': ReleaseType.season},
        {'label': 'SD Episode', 'value': '4', 'type': ReleaseType.episode},
        {'label': 'SD Movie', 'value': '2', 'type': ReleaseType.movie},
    )

    _category_value_type_map = {
        c['value']: c['type']
        for c in _categories
    }

    def autodetect_category(self, _):
        # "HD" or "SD"
        if (
            utils.video.height(self.content_path) >= 720
            or utils.video.width(self.content_path) >= 1280
        ):
            resolution = 'HD'
        else:
            resolution = 'SD'

        # "Movie", "Episode" or "Season"
        if self.release_name.type is ReleaseType.movie:
            typ = 'Movie'
        elif self.release_name.type is ReleaseType.season:
            typ = 'Season'
        elif self.release_name.type is ReleaseType.episode:
            typ = 'Episode'
        else:
            raise RuntimeError(f'Unsupported type: {self.release_name.type}')

        category = f'{resolution} {typ}'
        _log.debug('Autodetected category: %r', category)
        return category

    def propagate_category(self, _):
        release_type = self._category_value_type_map[self.category_job.choice]
        for job in (self.tmdb_job, self.tvmaze_job):
            if job.is_enabled:
                setattr(job.query, 'type', release_type)
                _log.debug('%s: New query: %r', job.name, job.query)

        self.release_name.type = release_type
        _log.debug('New release type: %s: %s', release_type, self.release_name)

    @cached_property
    def tmdb_job(self):
        tmdb_job = super().tmdb_job
        tmdb_job.no_id_ok = True
        tmdb_job.prejobs = [self.category_job]
        tmdb_job.condition = self.make_job_condition(
            'tmdb_job',
            appropriate_release_types=(
                ReleaseType.movie,
            ),
        )
        return tmdb_job

    @cached_property
    def tvmaze_job(self):
        tvmaze_job = super().tvmaze_job
        tvmaze_job.no_id_ok = True
        tvmaze_job.prejobs = [self.category_job]
        tvmaze_job.condition = self.make_job_condition(
            'tvmaze_job',
            appropriate_release_types=(
                ReleaseType.season,
                ReleaseType.episode,
            ),
        )
        return tvmaze_job

    def make_job_condition(self, job_attr, *, appropriate_release_types=()):
        """
        Return :attr:`~.base.JobBase.condition` for jobs

        Same as :meth:`~TrackerJobsBase.make_job_condition`, but also take
        release type into account: Job is only enabled if :attr:`release_name`
        is of a :attr:`~.ReleaseName.type` in `appropriate_release_types` or if
        `appropriate_release_types` is empty.
        """
        parent_condition = super().make_job_condition(job_attr)

        def condition():
            if parent_condition():

                def category_is_appropriate():
                    if self.category_job.is_finished:
                        choice = self.get_job_attribute(self.category_job, 'choice')
                        release_type = self._category_value_type_map.get(choice)
                        return release_type in appropriate_release_types

                return (
                    # Job is enabled regardless of release type
                    not appropriate_release_types
                    # Job is enabled if user-specified category is appropriate for this job
                    or category_is_appropriate()
                )

        return condition

    release_name_separator = '.'

    @cached_property
    def title_job(self):
        """Same as :attr:`~.TrackerJobsBase.release_name_job`"""
        return self.release_name_job

    @cached_property
    def description_job(self):
        # Don't cache job output because the number of screenshots can be
        # changed by the user between runs.
        job = jobs.dialog.TextFieldJob(
            name=self.get_job_name('description'),
            label='Description',
            condition=self.make_job_condition('description_job'),
            read_only=True,
            hidden=True,
            **self.common_job_args(ignore_cache=True)
        )
        job.add_task(
            job.fetch_text(
                coro=self.generate_description(),
                finish_on_success=True,
            )
        )
        return job

    async def generate_description(self):
        # Wait until all screenshots are uploaded
        await self.mediainfo_job.wait()
        await self.upload_screenshots_job.wait()

        mediainfo = (
            '[mediainfo]'
            + self.get_job_output(self.mediainfo_job, slice=0)
            + '[/mediainfo]'
        )

        screenshots = []
        for screenshot in self.upload_screenshots_job.uploaded_images:
            screenshots.append(f'[img]{screenshot}[/img]')

        screenshots_wrapped = (
            '[spoiler=Screenshots][center]'
            + '\n'.join(screenshots)
            + '[/center][/spoiler]'
        )

        promotion = (
            '[align=right][size=1]'
            f'Shared with [url={__homepage__}]{__project_name__}[/url]'
            '[/size][/align]'
        )

        return (
            mediainfo
            + '\n\n'
            + screenshots_wrapped
            + '\n\n'
            + promotion
        )

    @property
    def post_data_autofill(self):
        return {
            'submit': 'true',
            'MAX_FILE_SIZE': '2097152',
            'fillonly': 'auto fill',
            'category': '0',
            'Resolution': '0',
            'source': '12',
            'origin': '6',
            'title': '',
            'genre_tags': '---',
            'taglist': '',
            'autocomplete_toggle': 'on',
            'image': '',
            'fontfont': '-1',
            'fontsize': '-1',
            'desc': '',
            'fontfont': '-1',
            'fontsize': '-1',
            'groupDesc': '',
            'anonymous': '0',
        }

    @property
    def post_data_upload(self):
        return {
            'submit': 'true',
            'category': self.get_job_attribute(self.category_job, 'choice'),
            'Resolution': '0',
            'source': '12',
            'origin': '6',
            'title': self.get_job_output(self.title_job, slice=0),
            'genre_tags': '---',
            'autocomplete_toggle': 'on',
            'image': '',
            'fontfont': '-1',
            'fontsize': '-1',
            'desc': self.get_job_output(self.description_job, slice=0),
            'fontfont': '-1',
            'fontsize': '-1',
            'groupDesc': '',
            'anonymous': '1' if self.options['anonymous'] else '0',
            'ignoredupes': '1' if self.options['ignore_dupes'] else None,
            'tmdbid': self.get_job_output(self.tmdb_job, slice=0, default=None),
            # 'tmdbid': ...,
            # 'thetvdbid': ...,
            'tvmazeid': self.get_job_output(self.tvmaze_job, slice=0, default=None),
        }

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)
