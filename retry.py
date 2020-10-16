import logging
from datetime import datetime, timedelta

from apscheduler.events import EVENT_JOB_EXECUTED, JobExecutionEvent
from apscheduler.schedulers.base import BaseScheduler


class JobMisfireError(RuntimeError):
    pass


def enable_job_retry(
    scheduler: BaseScheduler,
    retry_delay: timedelta,
    max_retries: int,
    logger: logging.Logger = logging.getLogger("apscheduler"),
):
    if retry_delay < timedelta(seconds=1):
        raise ValueError("retry_delay must be positive")
    if max_retries <= 0:
        raise ValueError("max_retries must be positive")
    jobstores = scheduler._jobstores
    retry_counts = {
        jobstore: {job.id: 0 for job in scheduler.get_jobs(jobstore)}
        for jobstore in jobstores
    }

    def listener(event: JobExecutionEvent):
        job_id = event.job_id
        jobstore = event.jobstore
        retries = retry_counts[jobstore][job_id]

        if type(event.retval) == JobMisfireError:
            # job failed due to a misfire
            if retries < max_retries:
                # next retry
                retry_counts[jobstore][job_id] += 1
                logger.info(
                    "job %s failed. will retry in %s (%d/%d retry %s)",
                    job_id,
                    retry_delay,
                    retries + 1,
                    max_retries,
                    "attempt" if max_retries == 1 else "attempts",
                )
                scheduler.modify_job(
                    job_id=job_id,
                    jobstore=jobstore,
                    next_run_time=datetime.utcnow() + retry_delay,
                )
            else:
                # max retries reached
                logger.warning(
                    "job %s failed after %s",
                    job_id,
                    "1 retry" if retries == 1 else f"{retries} retries",
                )
                # reset retry_count
                retry_counts[jobstore][job_id] = 0
        elif retries > 0:
            # job executed successfully after retrying
            logger.info(
                "job %s executed successfully after %s",
                job_id,
                "1 retry" if retries == 1 else f"{retries} retries",
            )
            # reset retry_count
            retry_counts[jobstore][job_id] = 0

    scheduler.add_listener(listener, EVENT_JOB_EXECUTED)
