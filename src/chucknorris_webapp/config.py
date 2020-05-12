import typing
import os
from cached_property import cached_property

__all__ = (
    'WebappConfig',
)


class WebappConfig:
    @cached_property
    def CACHE_TYPE(self):
        # type: () -> typing.Optional[str]
        return os.environ.get('CACHE_TYPE', 'simple')

    @cached_property
    def CACHE_NO_NULL_WARNING(self):
        # type: () -> bool
        return True
