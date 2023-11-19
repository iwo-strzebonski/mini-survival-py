# pylint: disable=consider-using-f-string

from typing import Union, List, Any

from minisurvival.utils.config import Config
from minisurvival.utils.requests import request


class RedisClient:
    __rest_url = ""
    __rest_token = ""

    def __init__(self):
        config = Config()

        self.__rest_url = config.REDIS_REST_URL
        self.__rest_token = config.REDIS_REST_TOKEN

    def get(self, key):
        # type: (str) -> Union[dict[str, Any], str]
        """Get the value for the given key."""

        return request(
            "{}/get/{}".format(self.__rest_url, key),
            headers={"Authorization": "Bearer {}".format(self.__rest_token)},
        )

    def set(self, key, value):
        # type: (str, Union[dict[str, Any], str]) -> Union[dict[str, Any], str]

        """Set the value for the given key."""

        return request(
            "{}/set/{}/{}".format(self.__rest_url, key, value),
            headers={"Authorization": "Bearer {}".format(self.__rest_token)},
        )
