from .version import get_version

VERSION = (2, 2, 1, 'final', 0)

__version__ = get_version(VERSION)

from . import expressions  # NOQA
