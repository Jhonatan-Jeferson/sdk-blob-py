from typing import Literal


class MIMEType:
    """Class to handle blob supported MIME types."""
    MimeType = Literal[
    'video/mp4', 'video/mpeg',
    'video/webm', 'video/x-flv',
    'video/x-m4v', 'image/jpeg',
    'image/jpeg', 'image/png',
    'image/apng', 'image/tiff',
    'image/gif', 'image/webp',
    'image/bmp', 'image/svg+xml',
    'image/vnd.microsoft.icon', 'image/x-icon',
    'image/heic', 'image/heif',
    'audio/mpeg', 'audio/wav',
    'audio/ogg', 'audio/opus',
    'audio/aac', 'text/plain',
    'text/html', 'text/css',
    'text/csv', 'application/x-sql',
    'application/xml', 'application/x-sql',
    'application/x-sqlite3', 'application/pdf',
    'application/json', 'application/javascript',
    'application/x-pkcs12'
    ]
    extensions: tuple[str, ...] = (
        'mp4', 'mpeg',
        'webm', 'flv',
        'm4v', 'jpeg',
        'jpg', 'png',
        'apng', 'tiff',
        'gif', 'webp',
        'bmp', 'svg',
        'ico', 'cur',
        'heic', 'heif',
        'mp3', 'wav',
        'ogg', 'opus',
        'aac', 'txt',
        'html', 'css',
        'csv', 'x-sql',
        'xml', 'sql',
        'sqlite3', 'pdf',
        'json', 'js',
        'p12'
    )

    @staticmethod
    def is_valid(mimetype: str) -> bool:
        """Check if the mimetype is valid."""
        return mimetype in MIMEType.MimeType.__args__

    @staticmethod
    def get_mimetype(extension: str) -> str:
        """Get the mimetype from the file extension."""
        mapping = dict(zip(MIMEType.extensions, MIMEType.MimeType.__args__))
        return mapping.get(extension.lower(), "text/plain")
    
    @staticmethod
    def convert_to_extension(mimetype: str) -> str:
        """Convert a mimetype to a file extension."""
        mapping = dict(zip(MIMEType.MimeType.__args__, MIMEType.extensions))
        return mapping.get(mimetype.lower(), "txt")
