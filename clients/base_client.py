import requests

class BaseClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token

    def _get(self, path, **kwargs):
        return requests.get(url=f"{self.base_url}{path}", **self._with_token(kwargs))

    def _post(self, path, **kwargs):
        return requests.post(url=f"{self.base_url}{path}", **self._with_token(kwargs))

    def _delete(self, path, **kwargs):
        return requests.delete(url=f"{self.base_url}{path}", **self._with_token(kwargs))

    def _with_token(self, kwargs):
        if self.token is not None:
            kwargs.setdefault("cookies", {"token": self.token})
        return kwargs