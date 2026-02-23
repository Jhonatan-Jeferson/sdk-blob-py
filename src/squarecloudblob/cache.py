import asyncio 
from .data.blob_object import BlobObject
from .data.blob_stats import Stats


class Cache(object):
    """A Cache object that represents the cache of your account related with the Square Cloud Blob storage."""
    __slots__ = ("objects", "stats", "__scheduled_auto_clean")
    
    def __init__(self, clean_interval: float) -> None:
        self.objects: set[BlobObject] = set()
        self.stats: Stats | None = None
        self.__scheduled_auto_clean = asyncio.create_task(self.__auto_clean(clean_interval))

    def clear(self) -> None: 
        """Clear the cache."""
        self.objects.clear()
        self.stats = None
    
    async def __auto_clean(self, timer: float) -> None:
        try: 
            while not self.__scheduled_auto_clean.cancelled():
                await asyncio.sleep(timer)
                self.clear()
        except asyncio.CancelledError:
            pass