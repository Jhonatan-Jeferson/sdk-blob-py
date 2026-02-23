from aiohttp import ClientSession, ClientResponse
from datetime import date, datetime, timezone
from ..utils.file import File


class BlobObject(object):
    """A blob object represents a file stored in the Square Cloud Blob storage."""
    __slots__ = ("id", "size", "__created_at", "__expire_at")
    
    def __init__(self, id: str, size: int, **kwargs) -> None: 
        self.id: str = id
        self.size: int = size
        self.__created_at: str = kwargs.get("createdAt", datetime.now(timezone.utc).isoformat())
        self.__expire_at: str | None = kwargs.get("expireAt", None)
    
    @property
    def prefix(self) -> str:
        """The prefix of the blob object. If not found, returns an empty string."""
        splitted = self.id.split("/")
        if len(splitted) < 3:
            return ""
        return splitted[0]
    
    @property
    def name(self) -> str:
        """The name and hash of the blob object without the extension."""
        splitted = self.id.split("/")[-1].split(".")
        return splitted[-2]
    
    @property
    def extension(self) -> str:
        """The file extension of the blob object."""
        splitted = self.id.split(".")[-1]
        return splitted
    
    @property
    def url(self) -> str: 
        """The public URL of the blob object."""
        return f"https://public-blob.squarecloud.dev/{self.id}"

    @property
    def created_at(self) -> datetime:
        """The date and time when the blob object was created."""
        return datetime.fromisoformat(self.__created_at)
    
    @property
    def expire_at(self) -> datetime | None:
        """The date and time when the blob object expires."""
        if not self.__expire_at:
            return None
        return datetime.fromisoformat(self.__expire_at)
    
    async def download(self) -> File:
        """Download the blob object and return it as file object."""
        async with ClientSession() as session:
            response = await session.get(self.url)
            content = await response.read()
            file = File(content, response.headers["content-type"])
            response.close()
            return file