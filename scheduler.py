from datetime import timedelta

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

import jobs
import settings

jobstores = {"default": SQLAlchemyJobStore(url=settings.SQLALCHEMY_JOB_STORE)}
executors = {"default": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": True, "max_instances": 1, "misfire_grace_time": 300}
scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc,
)

for job in jobs.all_jobs:
    scheduler.add_job(
        func=job.function, id=job.id, trigger=job.trigger, replace_existing=True
    )

if settings.JOB_MAX_RETRIES > 0:
    from retry import enable_job_retry

    enable_job_retry(
        scheduler, timedelta(seconds=settings.JOB_RETRY_DELAY), settings.JOB_MAX_RETRIES
    )
