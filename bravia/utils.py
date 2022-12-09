from typing import List

from requests import Response


def handle_error(resp: Response) -> List[dict]:
    """
    Helper to check for and return the error
    if it exists in the response.

    :param resp: :class:`Response` object
    :type resp: :class:`Response`

    :rtype: List[dict]
    """

    if resp.json().get("error"):
        return resp.json()

    return resp.json().get("result")
