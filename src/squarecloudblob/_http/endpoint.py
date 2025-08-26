from typing import cast


class APIEndpoint(object):
    """
    Represents an API endpoint with a base URL and a path.
    """
    BASE_URL = "https://blob.squarecloud.app/v1"
    ENDPOINTS = {
        "ACCOUNT": {"path": "/account/stats", "methods": ["GET"]},
        "OBJECTS": {"path": "/objects", "methods": ["GET", "POST", "DELETE"]},
    }
    __slots__ = ("method", "path")

    def __init__(self, name: str, method: str):
        details: dict[str, list[str]|str] = self.ENDPOINTS[name.upper()]
        method = method.upper()
        if method not in details["methods"]:
            raise ValueError(f"Method {method} is not allowed for endpoint {details['path']}")
        self.method: str = method
        self.path: str = cast(str, details["path"])
        
    def __eq__(self, other: object) -> bool:
        return (isinstance(other, APIEndpoint) and self.method == other.method and self.path == other.path)

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        """
        Returns a string representation of the APIEndpoint instance.
        """
        return f"APIEndpoint(method={self.method}, path={self.path})"
    
    @property
    def url(self) -> str:
        """
        Returns the full URL for the API endpoint.
        """
        return f"{self.BASE_URL}{self.path}"