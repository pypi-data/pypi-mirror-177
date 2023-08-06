from pathlib import Path

import httpx
import pytest

from infiniaml_idp_client.schemas import Job, JobStatus, ProcessedJobWithResults
from tests.generated_models import JobInput

from ..conftest import AsyncJobClient, Config

FILENAME = "google-invoice.pdf"
FILEPATH = (Path(__file__) / "../../data/" / FILENAME).resolve()


async def _create_job(async_job_client: AsyncJobClient) -> Job:
    with FILEPATH.open("rb") as doc:
        return await async_job_client.create(JobInput(document=doc))


async def _process_job(async_job_client: AsyncJobClient):
    with FILEPATH.open("rb") as doc:
        return await async_job_client.process({"document": doc}, max_time=60)


class TestJobClient:
    @pytest.fixture(scope="class")
    async def created_job(self, async_job_client: AsyncJobClient):
        return await _create_job(async_job_client)

    @pytest.fixture(scope="class")
    async def created_job_2(self, async_job_client: AsyncJobClient):
        return await _create_job(async_job_client)

    @pytest.fixture(scope="class")
    async def created_completed_job(self, async_job_client: AsyncJobClient):
        return await _process_job(async_job_client)

    def test_create_success(self, created_job: Job, config: Config):
        assert created_job["project_id"] == config.project_id
        assert created_job["inputs"][0]["document"] == FILENAME

    def test_create_success_wait_until_complete(self, created_completed_job: ProcessedJobWithResults, config: Config):
        assert created_completed_job["project_id"] == config.project_id
        assert created_completed_job["inputs"][0]["document"] == FILENAME
        assert created_completed_job["status"] != JobStatus.PROCESSING

    async def test_get(self, async_job_client: AsyncJobClient, created_job: Job):
        job_with_results = await async_job_client.get(created_job["uuid"])
        assert job_with_results
        assert job_with_results["uuid"] == created_job["uuid"]

    async def test_get_not_found(self, async_job_client: AsyncJobClient):
        with pytest.raises(httpx.HTTPStatusError):
            await async_job_client.get("someuuidthatdoesntexist")

    async def test_iter_paginated_list(self, created_job: Job, created_job_2: Job, async_job_client: AsyncJobClient):
        uuids = [created_job["uuid"], created_job_2["uuid"]]
        items = await async_job_client.list(count=1, uuids=uuids)
        fetched_uuids = [job["uuid"] async for job in items]
        assert set(fetched_uuids) == set(uuids)

    async def test_iter_paginated_list_by_page(
        self, created_job: Job, created_job_2: Job, async_job_client: AsyncJobClient
    ):
        uuids = [created_job["uuid"], created_job_2["uuid"]]
        items = await async_job_client.list(count=1, uuids=uuids)
        fetched_uuids = [job["uuid"] async for page in items.by_page() for job in page]
        assert set(fetched_uuids) == set(uuids)
