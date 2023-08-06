import os

import requests
from aiohttp import ClientSession, ClientTimeout


class URLRequest:
    """
        Synchronous HTTP requests handler based on requests.

        Args:
            url (str): Base URL for the requests.
    """
    def __init__(self, url):
        self.url = url

    def get(self, **kwargs):
        """ Sends a GET request. """
        return requests.get(self.url, **kwargs)

    def post(self, **kwargs):
        """ Sends a POST request. """
        return requests.post(self.url, **kwargs)

    def delete(self, **kwargs):
        """ Sends a DELETE request. """
        return requests.delete(self.url, **kwargs)

    def put(self, **kwargs):
        """ Sends a PUT request. """
        return requests.put(self.url, **kwargs)

    def patch(self, **kwargs):
        """ Sends a PATCH request. """
        return requests.patch(self.url, **kwargs)

    def __getattr__(self, k):
        return URLRequest(os.path.join(self.url, k))

    def __getitem__(self, k):
        return URLRequest(os.path.join(self.url, k))

class AsyncURLRequest:
    """
        Synchronous HTTP requests handler based on aiohttp.

        Args:
            url (str): Base URL for the requests.
            timeout (float): The maximal number of seconds for the whole operation including connection establishment,
                request sending and response reading. Default: 300
    """
    def __init__(self, url, timeout=None):
        self.url = url
        self.timeout = timeout
    async def request(self, method='GET', **kwargs):
        """
            Sends a request.

            Args:
                method (str): Request method: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``,
                    or ``DELETE``.
        """
        async with ClientSession(timeout=ClientTimeout(total=self.timeout)) as session:
            return await session.request(url=self.url, method=method, **kwargs)

    def __getattr__(self, k):
        return AsyncURLRequest(os.path.join(self.url, k))

    def __getitem__(self, k):
        return AsyncURLRequest(os.path.join(self.url, k))
