from aiohttp import (ClientSession as http)

from .data.blob_object import BlobObject
from .data.blob_stats import Stats

from ._http import APIEndpoint
from .utils.file import File
from .cache import Cache

from typing import AsyncGenerator, cast
import asyncio

type Data = dict[str, str| dict[str, int|str]]

class Client(object):
    """Client for SquareCloud Blob API."""
    __headers = {
        "User-Agent": "squarecloud-blob-sdk-py/1.0"
    }
    __slots__ = ("cache", "__last_continuation_token")

    def __init__(self, api_key: str, cache_time: float=120.0) -> None:
        self.__headers.update({"Authorization": api_key})
        self.__last_continuation_token: str | None = None
        self.cache = Cache(cache_time)
    
    async def _request(self, endpoint: APIEndpoint, **kwargs) -> Data:
        """Make an HTTP request."""
        async with http(headers=self.__headers) as session:
            async with session.request(
                method=endpoint.method,
                url=endpoint.url,
                **kwargs
            ) as response:
                return await response.json()
            
    async def upload_object(
        self, 
        file: File, name: str, prefix: str|None=None,
        auto_download: bool=False, expires: int | None=None,
        security_hash: bool=False
    ) -> BlobObject:
        """Upload an object to the SquareCloud Blob API."""
        params: dict[str, str|int] = {
            "name": name,
            "auto_download": str(auto_download).lower(),
            "security_hash": str(security_hash).lower()
        }
        if expires:
            if 0 < expires < 365:
                params.update({"expires": expires})
        if prefix:
            params.update({"prefix": prefix})
        request = await self._request(APIEndpoint("OBJECTS", "POST"), params=params, data=file)
        response: dict = cast(dict, request.get("response", {}))
        return BlobObject(**response)

    async def fetch_account_info(self) -> Stats:
        """Fetch account information from the SquareCloud Blob API."""
        response: dict = await self._request(APIEndpoint("ACCOUNT", "GET"))
        account_info = Stats(**response)
        self.cache.stats = account_info
        return account_info

    async def fetch_objects(self, prefix: str|None=None, cache: bool=False) -> AsyncGenerator[list[BlobObject], None]:
        """Fetch objects from the SquareCloud Blob API."""
        _continue_loop = True
        while _continue_loop:
            params = {}
            if prefix: params.update({"prefix": prefix})
            if self.__last_continuation_token: params.update({"continuationToken": self.__last_continuation_token})
            response = await self._request(APIEndpoint("OBJECTS", "GET"), params=params)
            self.__last_continuation_token = cast(str|None, response.get("continuationToken", None))
            dict_objects: list[dict] = cast(list[dict], response["objects"])
            objects = [BlobObject(**obj) for obj in dict_objects]
            del dict_objects
            if cache: 
                self.cache.objects.clear()
                self.cache.objects.update(objects)
            yield objects
            await asyncio.sleep(1)
            if not self.__last_continuation_token: _continue_loop = False

    async def fetch_all_objects(self) -> list[BlobObject]:
        _gen = self.fetch_objects()
        object_list: list[BlobObject] = []
        while True:
            try: object_list.extend(await anext(_gen))
            except StopAsyncIteration: break
        return object_list

    async def get_objects(self, prefix: str|None=None) -> list[BlobObject]:
        """Get objects from cache."""
        if len(self.cache.objects) == 0: 
            await anext(self.fetch_objects(prefix, cache=True))
            return list(self.cache.objects)
        if not prefix: return list(self.cache.objects)
        return [obj for obj in self.cache.objects if obj.prefix == prefix]
    
    async def get_account_info(self) -> Stats:
        """Get account information from cache."""
        account_info = self.cache.stats
        if not account_info:
            account_info = await self.fetch_account_info()
        return account_info

    async def delete_object(self, id: str) -> bool:
        """Delete an object from the SquareCloud Blob API."""
        response = await self._request(APIEndpoint("OBJECTS", "DELETE"), json={"object": id})
        if response.get("status", "") != "success":
            raise Exception("Failed to delete object.")
        return True

    async def delete_objects(self, ids: list[str]) -> bool:
        """Delete multiple objects from the SquareCloud Blob API."""
        while (len(ids) > 0):
            await self.delete_object(ids.pop(0))
            await asyncio.sleep(1.5)
        return True