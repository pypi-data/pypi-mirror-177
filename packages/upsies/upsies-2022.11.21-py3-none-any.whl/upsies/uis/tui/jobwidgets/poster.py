from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.containers import ConditionalContainer

from ....utils import cached_property
from .. import widgets
from . import JobWidgetBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PosterJobWidget(JobWidgetBase):
    def setup(self):
        self._activity_indicator = widgets.ActivityIndicator(
            style='class:info',
            extend_width=True,
        )
        self.job.signal.register('finished', lambda _: self._activity_indicator.disable())

        self.job.signal.register('finding_poster', self.handle_finding_poster)
        self.job.signal.register('downloading_poster', self.handle_downloading_poster)
        self.job.signal.register('resizing_poster', self.handle_resizing_poster)
        self.job.signal.register('uploading_poster', self.handle_uploading_poster)
        self.job.signal.register('uploaded_poster', self.handle_uploaded_poster)

    def handle_finding_poster(self, id):
        self._activity_indicator.format = f'{{indicator}} Searching {id}'
        self._activity_indicator.active = True

    def handle_downloading_poster(self, url):
        self._activity_indicator.format = f'{{indicator}} Downloading {url}'

    def handle_resizing_poster(self, filepath):
        self._activity_indicator.format = f'{{indicator}} Resizing {filepath}'

    def handle_uploading_poster(self, filepath):
        self._activity_indicator.format = f'{{indicator}} Uploading {filepath}'

    def handle_uploaded_poster(self, url):
        self._activity_indicator.active = False
        self.invalidate()

    @cached_property
    def runtime_widget(self):
        return ConditionalContainer(
            filter=Condition(lambda: self._activity_indicator.active),
            content=self._activity_indicator,
        )
