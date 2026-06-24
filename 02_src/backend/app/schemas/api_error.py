from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ApiErrorBody(BaseModel):
    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] = {}


class ApiErrorResponse(BaseModel):
    error: ApiErrorBody


class ApiError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        status_code: int = 400,
        field: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.field = field
        self.details = details or {}
