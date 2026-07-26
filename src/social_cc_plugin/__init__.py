"""Cross-client installer for the Social Scientist skill library."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("social-cc-plugin")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "5.0.0"
