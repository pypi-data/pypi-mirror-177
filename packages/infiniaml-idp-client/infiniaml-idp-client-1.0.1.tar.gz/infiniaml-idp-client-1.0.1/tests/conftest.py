import asyncio

import pytest
from pydantic import BaseSettings

from infiniaml_idp_client import JobClient, aio
from infiniaml_idp_client._http_client_mixin import HttpClientMixin
from infiniaml_idp_client.aio._http_client_mixin import (
    HttpClientMixin as AsyncHttpClientMixin,
)
from infiniaml_idp_client.credentials import AccessKeyCredentials


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


class Config(BaseSettings):
    idp_url: str
    project_id: int
    access_key_id: str
    access_key_secret: str

    class Config:  # type: ignore
        env_prefix = "client_library_test_"
        env_file = ".env"


@pytest.fixture(scope="session")
def config():
    return Config.parse_obj({})


@pytest.fixture(scope="class")
async def async_creds(config: Config):
    async with aio.AccessKeyCredentials(
        config.access_key_id, config.access_key_secret, idp_url=config.idp_url
    ) as creds:
        yield creds


@pytest.fixture(scope="class")
async def async_job_client(config: Config, async_creds: aio.AccessKeyCredentials):
    async with aio.JobClient(config.project_id, async_creds, idp_url=config.idp_url) as job_client:
        yield job_client


@pytest.fixture(scope="class")
def creds(config: Config):
    return AccessKeyCredentials(config.access_key_id, config.access_key_secret, idp_url=config.idp_url)


@pytest.fixture(scope="class")
def job_client(config: Config, creds: AccessKeyCredentials):
    return JobClient(config.project_id, creds, idp_url=config.idp_url)


@pytest.fixture
def async_http_client_mixin():
    return AsyncHttpClientMixin()


@pytest.fixture
def http_client_mixin():
    return HttpClientMixin()


AsyncJobClient = aio.JobClient
