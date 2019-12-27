from pytz import utc

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

import jobs

jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")}
executors = {"default": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": False, "max_instances": 3}
scheduler = BlockingScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc
)

for job in jobs.all_jobs:
    scheduler.add_job(job)

scheduler.start()
