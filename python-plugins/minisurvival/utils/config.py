"""_summary_

Raises:
    AttributeError: Not allowed attribute

Returns:
    _type_: _description_
"""

# pylint: disable=consider-using-f-string

# pylint: disable=unspecified-encoding
from os.path import abspath, sep

from typing import Any, Dict


keys = ["REDIS_REST_URL", "REDIS_REST_TOKEN"]


class Config:
    """Config class for the plugin."""

    REDIS_REST_URL = ""
    REDIS_REST_TOKEN = ""

    def __init__(self):
        # type: () -> None
        """Initialize the config class."""

        config = self.read_env()

        for key, value in config.items():
            setattr(self, key, value)

    def __hasattr__(self, name):
        # type: (str) -> bool

        """Check if the attribute exists."""

        if name not in keys:
            raise AttributeError("Attribute not allowed")

        return hasattr(self, name)

    def __str__(self):
        # type: () -> str

        """Return the string representation of the class."""

        return str(self.__dict__)

    def read_env(self):
        # type: () -> Dict[str, Any]

        """Read the config from the file."""

        env_vars = {}

        with open("{}.env".format(abspath(".") + sep), "r") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue

                key, value = line.strip().split("=", 1)

                if key not in keys:
                    continue

                env_vars[key] = value.replace('"', "")

        return env_vars

    def get_item(self, key):
        # type: (str) -> Any

        """Get the config record."""

        if key not in keys:
            raise AttributeError("Attribute not allowed")

        return getattr(self, key)

    def get_items(self):
        # type: () -> Dict[str, Any]

        """Get the config items."""

        return {
            key: self.get_item(key)
            for key in keys
            if self.__hasattr__(key) and self.get_item(key) is not None
        }
