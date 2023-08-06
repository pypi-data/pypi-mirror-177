from datetime import datetime
from functools import partial
from typing import Any, Dict, Iterable, List, Literal, Optional, Sequence, Union, cast

import backoff
import httpx
from pydantic import parse_obj_as
from typing_extensions import Self

from infiniaml_idp_client._common.constants import IDP_URL
from infiniaml_idp_client.schemas import (
    DeletedJob,
    Job,
    JobInput,
    JobStatus,
    JobWithResults,
    ProcessingJob,
)

from .credentials import TokenCredential
from .idp_client import IdpClient
from .paginator import PaginatedItem

__all__ = ("JobClient",)


class JobClient:
    def __init__(
        self,
        project_id: int,
        token_credential: TokenCredential,
        *,
        idp_url: str = IDP_URL,
    ) -> None:
        """A client-side logical representation of the IDP Jobs API.

        Use this client to process documents, query jobs, and
        consume their results.

        Args:
            project_id: The project ID where the jobs will be created.
            token_credential: A token credential instance used for authentication.
        """
        self._idp_client = IdpClient(token_credential, idp_url)
        self._project_id = project_id

    def __enter__(self) -> Self:
        self._idp_client.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self._idp_client.__exit__()

    def close(self) -> None:
        self._idp_client.close()

    def _project_path(self) -> str:
        return f"/api/v1/projects/{self._project_id}"

    def _jobs_path(self) -> str:
        return "/".join((self._project_path(), "jobs"))

    def _job_path(self, uuid: str) -> str:
        return "/".join((self._jobs_path(), uuid))

    def create(self, input: JobInput) -> ProcessingJob:
        """Create a new job.

        The selected document will be queued for processing,
        returning a job with status `PROCESSING`. In order to receive
        job results, this job will need to be polled until its status
        is updated.

        Args:
            input: A dictionary containing job inputs. This
                dictionary must contain the field `document`, a
                file object of the document selected for processing.
        """
        files = {"document": input["document"]}
        data = dict(input)
        data.pop("document")
        resp = self._idp_client.post(
            self._jobs_path(),
            data=data,
            files=files,
        )
        return parse_obj_as(ProcessingJob, resp.json()[0])

    def process(self, input: JobInput, *, max_time: float = float("inf")) -> JobWithResults:
        """Create a new job, waiting for it to be processed.

        Similar to [`JobClient.create`][infiniaml_idp_client.JobClient.create],
        this method will create a new job but will internally
        poll the job until its status is no longer `JobStatus.PROCESSING`.

        Args:
            input: A dictionary containing job inputs. This
                dictionary must contain the field `document`, a
                file object of the document selected for processing.
        """
        job = self.create(input)

        @backoff.on_exception(backoff.expo, ValueError, max_time=max_time)
        def inner():
            fetched_job = self.get(job["uuid"])
            if fetched_job["status"] == JobStatus.PROCESSING:
                raise ValueError("Job is still processing")
            elif fetched_job["status"] == JobStatus.DELETED:
                raise TypeError("Job has been deleted")
            return fetched_job

        return inner()

    def get(self, uuid: str) -> Union[JobWithResults, ProcessingJob, DeletedJob]:
        """Get a job by its UUID.

        Whether or not a job contains results is dependent on its status. Consult the
        [documentation](job_client/index.md#job-results) for more info.
        """
        resp = self._idp_client.get(self._job_path(uuid))
        return parse_obj_as(Union[JobWithResults, ProcessingJob, DeletedJob], resp.json())

    @backoff.on_exception(backoff.expo, ValueError, max_tries=20)
    def _get_completed(self, uuid: str):
        resp = self._idp_client.get(self._job_path(uuid))
        if resp.json().get("status") == JobStatus.PROCESSING:
            raise ValueError("Job is still processing")
        return resp.json()

    def _list_impl(
        self,
        page: int,
        count: int,
        *,
        status: Union[Optional[JobStatus], Iterable[JobStatus]] = None,
        status_filter: Literal["inclusive", "exclusive"] = "inclusive",
        created_before: Optional[datetime] = None,
        created_after: Optional[datetime] = None,
        uuids: Optional[Iterable[str]] = None,
    ) -> List[Job]:
        params: Dict[str, Any] = {
            "per": count,
            "page": page,
        }
        if status:
            params["status"] = status
            params["status_filter"] = status_filter
        if created_before:
            params["created_before"] = created_before
        if created_after:
            params["created_after"] = created_after
        if uuids:
            params["uuid"] = list(uuids)
        try:
            resp = self._idp_client.get(self._jobs_path(), params=params)
        except httpx.HTTPStatusError as err:
            if err.response.status_code == 404:
                return []
            raise
        return parse_obj_as(List[Job], resp.json()["jobs"])

    def list(
        self,
        *,
        count: int = 10,
        status: Union[Optional[JobStatus], Iterable[JobStatus]] = None,
        status_filter: Literal["inclusive", "exclusive"] = "inclusive",
        created_before: Optional[datetime] = None,
        created_after: Optional[datetime] = None,
        uuids: Optional[Iterable[str]] = None,
    ) -> PaginatedItem[Job]:
        """List jobs.

        A number of filters are included as parameters in order to retrieve
        a desired subset of jobs.

        Args:
            count: The number of jobs returned per page. Defaults to 10.
            status: Filter jobs by status(es). Defaults to None.
            status_filter: Whether or not to filter status(es) inclusively or
                exclusively. Defaults to "inclusive".
            created_before: Filter jobs that were created before a certain datetime.
            created_after: Filter jobs that were created after a certain datetime. Defaults to None.
            uuids: Filter jobs with provided UUID(s). Defaults to None.

        Returns:
            PaginatedItem[Job]: An iterable of jobs.
        """
        get_page = cast(
            _GetPage,
            partial(
                self._list_impl,
                count=count,
                status=status,
                status_filter=status_filter,
                created_before=created_before,
                created_after=created_after,
                uuids=uuids,
            ),
        )
        return PaginatedItem(_PageIncrementor(get_page))


class _GetPage:
    def __call__(self, *, page: int) -> Sequence[Job]:
        ...


class _PageIncrementor:
    def __init__(self, list_func: _GetPage) -> None:
        self._page = 1
        self._list_func = list_func

    def __call__(self) -> Sequence[Job]:
        job = self._list_func(page=self._page)
        self._page += 1
        return job
