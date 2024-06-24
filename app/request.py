from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Request:
    method: str
    target: str
    http_version: str
    headers: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_string(cls, request_string: str) -> "Request":
        """
        Create a Request instance from a string.

        Args:
            request_string (str): A string representation of the request.

        Returns:
            Request: An instance of the Request class.
        """
        line_ending = request_string.find("\r\n")
        status_line = request_string[:line_ending]
        headers: Dict[str, str] = {}

        for header_str in request_string[line_ending + 2 :].split("\r\n"):
            if header_str == "":
                break
            header, value = header_str.split(":", maxsplit=1)
            print(header + "  " + value)
            headers[header] = value.strip()

        method, target, version = status_line.split()

        return cls(method=method, target=target, http_version=version, headers=headers)

    @property
    def target_paths(self) -> list[str]:
        return self.target.split("/")
