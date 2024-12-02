import json
from typing import Any, Dict, List, Optional

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    IPvAnyAddress,
    ValidationError,
    field_validator,
)

from log_analyzer.utils.logger import get_logger

logger = get_logger(__name__)


class LogEntry(BaseModel):
    """
    Schema for log entry.
    """

    timestamp: Optional[float] = Field(
        None,
        description="Timestamp of the request in seconds since the epoch.",
    )
    response_header_size: Optional[int] = Field(
        None, ge=0, description="Response header size in bytes."
    )
    client_ip: Optional[IPvAnyAddress] = Field(
        None, description="IP address of the client."
    )
    http_response_code: Optional[int] = Field(
        None, ge=100, le=999, description="HTTP response code (1xx-5xx)."
    )
    response_size: Optional[int] = Field(
        None, ge=0, description="Size of the response in bytes."
    )
    http_method: Optional[str] = Field(
        None,
        pattern="^(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH|TRACE|CONNECT|PROPFIND)$",
        description="HTTP request method.",
    )
    url: Optional[HttpUrl] = Field(None, description="Requested URL.")
    username: Optional[str] = Field(
        None, description="Username or '-' if unauthenticated."
    )
    access_type: Optional[str] = Field(None, description="Access Type")
    destination_ip: Optional[IPvAnyAddress] = Field(
        None, description="Destination IP Address"
    )
    response_type: Optional[str] = Field(None, description="Response type.")

    @field_validator("url", mode="before")
    def prepend_http(cls, v: str) -> str:
        if isinstance(v, str) and not v.startswith("http"):
            return f"http://{v}"
        return v

    @classmethod
    def __clean(cls, value: str) -> Optional[str]:
        return None if value in ("NONE", "-") else value

    @classmethod
    def __split(cls, value: str, sep="/") -> tuple[Optional[str], Optional[str]]:
        if value and sep in value:
            first_half, second_half = value.split(sep)
            return cls.__clean(first_half), cls.__clean(second_half)
        return value, ""

    @classmethod
    def __row_to_dict(cls, row: List[str]) -> Dict[str, Any]:
        access_type, destination_ip = cls.__split(row[8])
        _, response_code = cls.__split(row[3])
        return dict(
            timestamp=float(row[0]),
            response_header_size=int(row[1]),
            client_ip=row[2],
            http_response_code=response_code,
            response_size=int(row[4]),
            http_method=row[5],
            url=row[6],
            username=row[7],
            access_type=access_type,
            destination_ip=destination_ip,
            response_type=row[9],
        )

    @classmethod
    def from_raw(cls, row: List[str], line_number: int) -> Dict[str, Any]:
        """
        Create a LogEntry from raw row data with automatic validation.

        :param row: List of raw field values.
        :param line_number: Current line number for logging.
        :return: Valid data dict.
        """
        row_dict: Dict[str, Any] = cls.__row_to_dict(row)
        valid_data = {}
        for field, value in row_dict.items():
            try:
                model = cls.model_validate({field: value})
                valid_data[field] = getattr(model, field)
            except ValidationError:
                # logger.debug("Unable to parse entry: %s, ERROR: %s", row, e)
                valid_data[field] = None
        return json.loads(cls(**valid_data).model_dump_json())
