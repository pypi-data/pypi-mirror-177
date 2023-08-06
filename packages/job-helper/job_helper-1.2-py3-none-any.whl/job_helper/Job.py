import uuid

from datetime import datetime
from job_helper.Status import Status


class Job:
    def __init__(
        self,
        job_type,
        job_info,
        asset_id=None,
        mediafile_id=None,
        parent_job_id=None,
        status=Status.QUEUED.value,
        completed_jobs=0,
        amount_of_jobs=1,
        user=None,
    ):
        self.end_time = None
        self.job_type = job_type
        self.job_info = job_info
        self.status = status
        self.start_time = str(datetime.utcnow())
        self.user = user if user else "default_uploader"
        self.asset_id = asset_id
        self.mediafile_id = mediafile_id
        self.parent_job_id = parent_job_id
        self.completed_jobs = completed_jobs
        self.amount_of_jobs = amount_of_jobs
        self.identifiers = [uuid.uuid1().hex]

    def count_up_completed_jobs(self):
        self.completed_jobs = self.completed_jobs + 1
