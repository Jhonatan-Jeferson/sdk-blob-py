from aiohttp import ClientSession


class BlobObject(object):
    """A blob object represents a file stored in the Square Cloud Blob storage."""
    
    __slots__ = ("id", "size")
    
    def __init__(self, id: str, size: int) -> None: 
        self.id: str = id
        self.size: int = size
    
    @property
    def prefix(self) -> str:
        """The prefix of the blob object. If not found, returns an empty string."""
        splitted = self.id.split("/")
        if len(splitted) < 3:
            return ""    
        return splitted[0]
    
    @property
    def name(self) -> str:
        """The name of the blob object without the extension and hash."""
        splitted = self.id.split("/")[-1].split("_")
        return "_".join(splitted[:-1])
    
    @property
    def extension(self) -> str:
        """The file extension of the blob object."""
        splitted = self.id.split(".")[-1]
        return splitted
    
    @property
    def url(self) -> str: 
        """The public URL of the blob object."""
        return f"https://public-blob.squarecloud.dev/{self.id}"
    
    async def download(self, path: str="/blobDownloads") -> None:
        """Download the blob object and save it in the specified path."""
        async with ClientSession() as session:
            async with session.get(self.url) as response:
                content = await response.read()
                with open(f"{path}/{self.name}.{self.extension}", "wb") as file:
                    file.write(content)