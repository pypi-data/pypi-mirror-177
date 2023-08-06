import requests


class SwapSession(requests.Session):
    """Swap Session Object
    https://github.com/wwt/building-a-python-sdk/tree/main/docs

    Args:
        requests (Session): Sub-classes requests.Session
    """

    def add_api_key(self, api_key):
        self.headers.update({"Content-Type": "application/json", "api_key": api_key})
