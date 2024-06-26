from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass
class Request:
    method: str
    target: str
    http_version: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = field(default=None)
    accept_encodings: Set[str] = field(default_factory=set)

    @classmethod
    def from_string(cls, request_string: str) -> "Request":
        """
        Create a Request instance from a string.

        Args:
            request_string (str): A string representation of the request.

        Returns:
            Request: An instance of the Request class.
        """
        status_line, *tail = request_string.split("\r\n")
        headers: Dict[str, str] = {}

        while (header_str := tail.pop(0)) != "":
            header, value = header_str.split(":", maxsplit=1)
            headers[header] = value.strip()

        accepted_encodings: Set[str] = set()
        if "Accept-Encoding" in headers:
            for encoding in headers.pop("Accept-Encoding").split(","):
                accepted_encodings.add(encoding.strip())

        method, target, version = status_line.split()
        body = "".join(tail)

        return cls(
            method=method,
            target=target,
            http_version=version,
            headers=headers,
            body=body,
            accept_encodings=accepted_encodings,
        )

    @property
    def target_paths(self) -> list[str]:
        return self.target.split("/")
