"""
Below are schemas that define the input/output types of client methods.
"""

from datetime import datetime
from enum import Enum
from typing import Any, BinaryIO, Dict, List, Literal, Union

from typing_extensions import TypedDict

__all__ = [
    "JobStatus",
    "Job",
    "JobInput",
    "JobWithResults",
]


class JobInput(TypedDict):
    """
    Attributes:
        document: The input document as a file object.
    """

    document: BinaryIO


class JobStatus(str, Enum):
    """
    Attributes:
        PROCESSING (str): The document is still processing and does not have results yet.
        PROCESSED (str): The document has been processed and results are available.
        PENDING_REVIEW (str): The document is pending review. The returned job should include a **content URL**
            linking to the document in the IDP UI where the user can review it.
        ERROR (str): The job has errored for some reason.
        DELETED (str): The job has been deleted.
    """

    PROCESSING = "Processing"
    PROCESSED = "Processed"
    PENDING_REVIEW = "Pending review"
    REVIEWED = "Reviewed"
    ERROR = "Error"
    DELETED = "Deleted"


class JobBase(TypedDict):
    """
    Attributes:
        uuid: Job UUID used to retrieve job.
        project_id: The project ID of the project associated with the job.
        created_at: The time the job was created.
        inputs: The list of inputs provided when the job was created.
    """

    uuid: str
    project_id: int
    created_at: datetime
    inputs: List[Dict[str, Any]]


class ProcessingJob(JobBase):
    """
    Attributes:
        status: Status is `"Processing"`.
    """

    status: Literal[JobStatus.PROCESSING]


class ProcessedJob(JobBase):
    """
    Attributes:
        status: Status is `"Processed"`.
        processed_at: The time the job completed processing.
    """

    status: Literal[JobStatus.PROCESSED]
    processed_at: datetime


class ErroredJob(JobBase):
    """
    Attributes:
        status: Status is `"Error"`
    """

    status: Literal[JobStatus.ERROR]


class DeletedJob(JobBase):
    """
    Attributes:
        status: Status is `"Deleted"`
    """

    status: Literal[JobStatus.DELETED]


class PendingReviewJob(JobBase):
    """
    Attributes:
        status: Status is `"Pending review"`
        content_url: A link to the IDP document UI where a user can review the document.
    """

    status: Literal[JobStatus.PENDING_REVIEW]
    content_url: str


class ReviewedJob(JobBase):
    """
    Attributes:
        status: Status is `"Reviewed"`
    """

    status: Literal[JobStatus.REVIEWED]


Job = Union[ProcessingJob, ProcessedJob, PendingReviewJob, ReviewedJob, ErroredJob, DeletedJob]


class ProcessedJobWithResults(ProcessedJob):
    """
    Attributes:
        results: List of results returned from processed job.
    """

    results: List[Dict[str, Any]]


class PendingReviewJobWithResults(PendingReviewJob):
    """
    Attributes:
        results: List of results returned from processed job.
    """

    results: List[Dict[str, Any]]


class ReviewedJobWithResults(ReviewedJob):
    """
    Attributes:
        results: List of results returned from processed job.
    """

    results: List[Dict[str, Any]]


class ErrorResult(TypedDict):
    """
    Attributes:
        error: A job error.
    """

    error: Dict[str, Any]


class ErroredJobWithResults(ErroredJob):
    """
    Attributes:
        results: List of errors returned from errored job.
    """

    results: List[ErrorResult]


JobWithResults = Union[ProcessedJobWithResults, PendingReviewJobWithResults, ErroredJobWithResults]
