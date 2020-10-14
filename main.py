from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc

import jobs
import settings

if not settings.DEBUG:
    import logging

    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s.%(funcName)s: %(message)s",
        datefmt=r"%H:%M:%S",
    )
    logging.getLogger("apscheduler").setLevel(logging.DEBUG)

jobstores = {"default": SQLAlchemyJobStore(url=settings.SQLALCHEMY_JOB_STORE)}
executors = {"default": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": True, "max_instances": 1, "misfire_grace_time": 300}
scheduler = BlockingScheduler(
    jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc
)
for job in jobs.all_jobs:
    scheduler.add_job(
        func=job.function, id=job.id, trigger=job.trigger, replace_existing=True
    )


def run():
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)
        exit(0)


if __name__ == "__main__":
    run()
