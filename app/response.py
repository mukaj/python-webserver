from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Response:
    status: int
    body: Optional[str] = field(default=None)
    http_version: str = field(default="1.1")
    headers: Dict[str, str] = field(default_factory=dict)

    STATUS_CODES = {
        200: "OK",
        404: "Not Found",
    }

    def send_response(self) -> bytes:
        response = b""
        response += b"HTTP/%b " % self.http_version.encode()
        response += b"%b %b" % (
            bytes(str(self.status), encoding="utf-8"),
            bytes(self.STATUS_CODES[self.status], encoding="utf-8"),
        )

        response += b"\r\n"
        for header, value in self.headers.items():
            header_row = f"{header}: {value}\r\n"
            response += bytes(header_row, encoding="utf-8")

        response += b"\r\n"
        if self.body:
            response += bytes(self.body, encoding="utf-8")

        return response
