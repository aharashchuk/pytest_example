"""HTTP status codes used across API tests."""

from enum import IntEnum


class StatusCodes(IntEnum):
    OK = 200
    CREATED = 201
    DELETED = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    CONFLICT = 409
    SERVER_ERROR = 500
