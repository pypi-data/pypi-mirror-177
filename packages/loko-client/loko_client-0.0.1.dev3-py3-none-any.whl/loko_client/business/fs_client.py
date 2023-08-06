from typing import Union, BinaryIO

from loko_client.business.base_client import OrchestratorClient, AsyncOrchestratorClient


class FSClient(OrchestratorClient):
    """
        Orchestrator client used to access to Loko data.

        Args:
            gateway (str): Gateway URL.
    """

    def ls(self, path: str):
        """
            List directory contents.

            Parameters:
                path (str): The path to the parent folder.

            Returns:
                List[dict]: List of contents.

        """
        r = self.u.files[path].get()
        return r.json()['items']

    def read(self, path: str, mode='rb'):
        """
            Read file.

            Parameters:
                path (str): The path to the file.
                mode (str): The mode in which the file is read. Available modes are: "r" and "rb". Default: 'rb'

            Returns:
                 Union[str, bytes]: File content.
        """
        r = self.u.files[path].get()
        if mode=='rb':
            return r.content
        return r.content.decode()

    def update(self, path: str, body: Union[bytes, BinaryIO]=None):
        """
            Update file.

            Parameters:
                path (str): The path to the file.
                body (Union[bytes, BinaryIO]): File's content.

        """
        r = self.u.files[path].post(data=body)
        return r.text

    def save(self, path: str, body: Union[bytes, BinaryIO]=None):
        """
            Save file or directory.

            Parameters:
                path (str): The path to the file.
                body (Union[bytes, BinaryIO]): File's content. `None` if you want to save a directory. Default: None

        """
        if body:
            r = self.u.files[path].post(data=body)
        else:
            r = self.u.files[path].post()
        return r.text

    def delete(self, path: str):
        """
            Delete file or directory.

            Parameters:
                path (str): The path to the file or directory.

        """
        r = self.u.files[path].delete()
        return r.text

    def copy(self, path: str, new_path: str):
        """
            Copy file or directory.

            Parameters:
                path (str): The path to the file or directory.
                new_path (str): The new path to the file or directory.

        """
        r = self.u.copy[path].post(json=dict(path=new_path))
        return r.text

    def move(self, path: str, new_path: str):
        """
            Move file or directory.

            Parameters:
                path (str): The path to the file or directory.
                new_path (str): The new path to the file or directory.

        """
        r = self.u.files[path].patch(json=dict(path=new_path))
        return r.text

class AsyncFSClient(AsyncOrchestratorClient):
    """
        Asynchronous Orchestrator client used to access to Loko data.

        Args:
            gateway (str): Gateway URL.
            timeout (float): The maximal number of seconds for the whole operation including connection establishment,
                request sending and response reading. Default: 300
    """

    def __init__(self, gateway, timeout=None):
        super().__init__(gateway, timeout)

    async def ls(self, path: str):
        """
            List directory contents.

            Parameters:
                path (str): The path to the parent folder.

            Returns:
                List[dict]: List of contents.

        """
        resp = await self.u.files[path].request('GET')
        r = await resp.json()
        return r['items']

    async def read(self, path: str, mode='rb', content=False):
        """
            Read file.

            Parameters:
                path (str): The path to the file.
                mode (str): The mode in which the file is read. Available modes are: "r" and "rb". Default: 'rb'
                content (bool): Set to `True` to return the response content. Default: False

            Returns:
                 Union[str, bytes, aiohttp.streams.StreamReader]: File content.
        """
        resp = await self.u.files[path].request('GET')
        _content = resp.content
        if content:
            return _content
        _content = await _content.read()
        if mode=='rb':
            return _content
        return _content.decode()

    async def update(self, path: str, body: Union[bytes, BinaryIO]=None):
        """
            Update file.

            Parameters:
                path (str): The path to the file.
                body (Union[bytes, BinaryIO]): File's content.

        """
        r = await self.u.files[path].request('POST', data=body)
        return await r.text()

    async def save(self, path: str, body: Union[bytes, BinaryIO]=None):
        """
            Save file or directory.

            Parameters:
                path (str): The path to the file.
                body (Union[bytes, BinaryIO]): File's content. `None` if you want to save a directory. Default: None

        """
        if body:
            r = await self.u.files[path].request('POST', data=body)
        else:
            r = await self.u.files[path].request('POST')
        return await r.text()

    async def delete(self, path: str):
        """
            Delete file or directory.

            Parameters:
                path (str): The path to the file or directory.

        """
        r = await self.u.files[path].request('DELETE')
        return await r.text()

    async def copy(self, path: str, new_path: str):
        """
            Copy file or directory.

            Parameters:
                path (str): The path to the file or directory.
                new_path (str): The new path to the file or directory.

        """
        r = await self.u.copy[path].request('POST', json=dict(path=new_path))
        return await r.text()

    async def move(self, path: str, new_path: str):
        """
            Move file or directory.

            Parameters:
                path (str): The path to the file or directory.
                new_path (str): The new path to the file or directory.

        """
        r = await self.u.files[path].request('PATCH', json=dict(path=new_path))
        return await r.text()
