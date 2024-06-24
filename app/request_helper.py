from dataclasses import dataclass


@dataclass
class Request:
    method: str
    target: str
    http_version: str

    @classmethod
    def from_string(cls, request_string: str) -> "Request":
        """
        Create a Request instance from a string.

        Args:
            request_string (str): A string representation of the request.

        Returns:
            Request: An instance of the Request class.
        """
        line, headers, body, _ = request_string.split("\r\n")
        method, target, version = line.split()

        return cls(method=method, target=target, http_version=version)
