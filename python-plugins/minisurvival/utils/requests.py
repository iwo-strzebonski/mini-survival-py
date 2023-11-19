# pylint: disable=consider-using-f-string

import json
from urllib import urlencode
import urllib2

from typing import Union, Dict, Any
from typing_extensions import Literal

MethodEnum = Literal["GET", "POST", "PUT", "DELETE"]


def request(
    url,
    method="GET",
    headers=None,
):
    # type: (str, MethodEnum, Union[Dict[str, str], None]) -> Any

    """Makes a request to the given url.

    Raises:
        URLError: Incorrect and possibly insecure protocol in url

    Returns:
        Response: Response object
    """

    if not url.startswith("http"):
        raise ValueError(
            "Incorrect and possibly insecure protocol in url: {}.".format(url)
        )

    headers = headers or {}
    headers.update({"Accept": "application/json"})

    httprequest = urllib2.Request(url, headers=headers)

    result = None

    try:
        httpresponse = urllib2.urlopen(httprequest)
        result = json.loads(httpresponse.read())["result"]
    except urllib2.HTTPError as error:
        result = {
            "code": error.code,
            "reason": error.reason,
        }

    return result
