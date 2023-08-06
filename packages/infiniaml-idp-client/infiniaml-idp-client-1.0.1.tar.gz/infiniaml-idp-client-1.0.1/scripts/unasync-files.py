import os
from pathlib import Path
from typing import List

import unasync

REPLACEMENTS = {
    "AsyncClient": "Client",
    "AsyncTokenCredential": "TokenCredential",
    "aclose": "close",
}

TEST_REPLACEMENTS = {
    "async_job_client": "job_client",
    "async_account_management_client": "account_management_client",
    "AsyncJobClient": "JobClient",
    "AsyncHttpClientMixin": "HttpClientMixin",
    "async_http_client_mixin": "http_client_mixin",
}

RULES = [
    unasync.Rule(
        fromdir="infiniaml_idp_client/aio",
        todir="infiniaml_idp_client/",
        additional_replacements=REPLACEMENTS,
    ),
    unasync.Rule(
        fromdir="tests/async",
        todir="tests/sync",
        additional_replacements=TEST_REPLACEMENTS,
    ),
]

ASYNC_DIRS = ["infiniaml_idp_client/aio", "tests/async"]


def _is_py_file_extension(filename: str):
    if filename.rpartition(".")[-1] in ("py", "pyi"):
        return True
    return False


def _get_async_filepaths(dir: str) -> List[str]:
    filepaths: List[str] = []
    for root, _, filenames in os.walk(Path(__file__).absolute().parent.parent / dir):
        for filename in filenames:
            if _is_py_file_extension(filename):
                filepaths.append(os.path.join(root, filename))
    return filepaths


def main():
    filepaths = [filepath for dir in ASYNC_DIRS for filepath in _get_async_filepaths(dir)]
    unasync.unasync_files(filepaths, RULES)


if __name__ == "__main__":
    main()
