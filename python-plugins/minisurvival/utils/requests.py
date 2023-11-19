import json
import urllib.error
import urllib.parse
import urllib.request
from email.message import Message

from typing import Any, List, Union, NamedTuple


class Response(NamedTuple):
    body: str
    headers: Message
    status: int
    error_count: int = 0

    def json(self):
        # type: () -> Union[dict, str, int, float, None, List]
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        try:
            output = json.loads(self.body)
        except json.JSONDecodeError:
            output = ""
        return output


def request(
    url,
    data=None,
    params=None,
    headers=None,
    method="GET",
    data_as_json=True,
    error_count=0,
) -> Response:
    # type: (str, Union[dict[str, Any], None], Union[dict[str, Any], None], Union[dict[str, Any], None], str, bool, int) -> Response

    """Makes a request to the given url.

    Raises:
        urllib.error.URLError: Incorrect and possibly insecure protocol in url

    Returns:
        Response: Response object
    """

    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")

    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if data_as_json:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except urllib.error.HTTPError as e:
        response = Response(
            body=str(e.reason),
            headers=e.headers,
            status=e.code,
            error_count=error_count + 1,
        )

    return response
