from __future__ import annotations

from typing import BinaryIO, Union

from typing_extensions import NotRequired, TypedDict


class JobInput(TypedDict):
    document: BinaryIO
    page_numbers: NotRequired[Union[int, str]]
    password: NotRequired[str]
    unique_uuid: NotRequired[str]
