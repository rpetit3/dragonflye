"""Top-level package for sccmec."""

from importlib import metadata

__version__ = metadata.version("dragonflye")
__author__ = metadata.metadata("dragonflye").get("author")
__url__ = metadata.metadata("dragonflye").get("home-page")
