from __future__ import annotations
from io import BufferedIOBase, BytesIO
from ..utils.mimetype import MIMEType

class File(object):
    __slots__ = ("bytes", "size", "__mimetype")
    MIN_SIZE = 1024
    MAX_SIZE = 100 * 1024 * 1024

    def __init__(self, content: bytes, mimetype: MIMEType.MimeType | str) -> None:
        self.verify_file(content, mimetype)
        self.bytes = content
        self.size = len(content)
        self.__mimetype = mimetype

    @classmethod
    def from_path(cls, path: str, mimetype: MIMEType.MimeType | str) -> File:
        """Create a File object from a file path."""
        file = open(path, "rb")
        content = file.read()
        file.close()
        return cls(content, mimetype)

    @classmethod
    def from_buffer(cls, buffer: BufferedIOBase | BytesIO, mimetype: MIMEType.MimeType | str) -> File:
        """Create a File object from a BufferedIOBase or BytesIO object."""
        content = buffer.read()
        return cls(content, mimetype)

    @property
    def mimetype(self) -> str:
        """Return the mimetype of the file."""
        return self.__mimetype

    def save_file(self, path: str) -> None:
        """Save the file to the specified path."""
        file = open(path, "wb")
        file.write(self.bytes)
        file.close()

    def verify_file(self, content: bytes, mimetype: str) -> None:
        """Verify if the file is valid for Blob storage."""
        if not (self.MIN_SIZE <= len(content) <= self.MAX_SIZE): raise Exception("File size must be between 1KB and 100MB.")
        if not MIMEType.is_valid(mimetype): raise Exception("Unsupported file mimetype.")
