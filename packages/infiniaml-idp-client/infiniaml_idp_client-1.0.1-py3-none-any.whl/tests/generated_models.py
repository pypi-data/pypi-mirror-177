from __future__ import annotations

from enum import Enum
from typing import BinaryIO, Union
from uuid import UUID

from typing_extensions import NotRequired, TypedDict


class OutputStatus(str, Enum):
    success = "success"
    needs_review = "needs_review"
    error = "error"


class JobInput(TypedDict):
    document: BinaryIO
    document_uuid: NotRequired[UUID]
    page_numbers: NotRequired[Union[int, str]]
    password: NotRequired[str]
    config: NotRequired[str]
    return_status: NotRequired[OutputStatus]
    return_message: NotRequired[str]
    return_document_model: NotRequired[str]
    return_keep_content: NotRequired[str]
