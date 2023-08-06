from __future__ import annotations

from typing import BinaryIO, List, Union

from typing_extensions import NotRequired, TypedDict


class ClientResult(TypedDict):
    currently_supported_drug: bool
    unique_uuid: NotRequired[str]


class JobInput(TypedDict):
    document: BinaryIO
    page_numbers: NotRequired[Union[int, str]]
    password: NotRequired[str]
    unique_uuid: NotRequired[str]


JobResults = List[ClientResult]
