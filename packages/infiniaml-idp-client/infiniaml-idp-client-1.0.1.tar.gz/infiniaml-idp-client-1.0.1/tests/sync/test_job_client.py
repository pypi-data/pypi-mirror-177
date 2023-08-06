from pathlib import Path

import httpx
import pytest

from infiniaml_idp_client.schemas import Job, JobStatus, ProcessedJobWithResults
from tests.generated_models import JobInput

from ..conftest import Config, JobClient

FILENAME = "google-invoice.pdf"
FILEPATH = (Path(__file__) / "../../data/" / FILENAME).resolve()


def _create_job(job_client: JobClient) -> Job:
    with FILEPATH.open("rb") as doc:
        return job_client.create(JobInput(document=doc))


def _process_job(job_client: JobClient):
    with FILEPATH.open("rb") as doc:
        return job_client.process({"document": doc}, max_time=60)


class TestJobClient:
    @pytest.fixture(scope="class")
    def created_job(self, job_client: JobClient):
        return _create_job(job_client)

    @pytest.fixture(scope="class")
    def created_job_2(self, job_client: JobClient):
        return _create_job(job_client)

    @pytest.fixture(scope="class")
    def created_completed_job(self, job_client: JobClient):
        return _process_job(job_client)

    def test_create_success(self, created_job: Job, config: Config):
        assert created_job["project_id"] == config.project_id
        assert created_job["inputs"][0]["document"] == FILENAME

    def test_create_success_wait_until_complete(self, created_completed_job: ProcessedJobWithResults, config: Config):
        assert created_completed_job["project_id"] == config.project_id
        assert created_completed_job["inputs"][0]["document"] == FILENAME
        assert created_completed_job["status"] != JobStatus.PROCESSING

    def test_get(self, job_client: JobClient, created_job: Job):
        job_with_results = job_client.get(created_job["uuid"])
        assert job_with_results
        assert job_with_results["uuid"] == created_job["uuid"]

    def test_get_not_found(self, job_client: JobClient):
        with pytest.raises(httpx.HTTPStatusError):
            job_client.get("someuuidthatdoesntexist")

    def test_iter_paginated_list(self, created_job: Job, created_job_2: Job, job_client: JobClient):
        uuids = [created_job["uuid"], created_job_2["uuid"]]
        items = job_client.list(count=1, uuids=uuids)
        fetched_uuids = [job["uuid"] for job in items]
        assert set(fetched_uuids) == set(uuids)

    def test_iter_paginated_list_by_page(self, created_job: Job, created_job_2: Job, job_client: JobClient):
        uuids = [created_job["uuid"], created_job_2["uuid"]]
        items = job_client.list(count=1, uuids=uuids)
        fetched_uuids = [job["uuid"] for page in items.by_page() for job in page]
        assert set(fetched_uuids) == set(uuids)
