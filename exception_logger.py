from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.base import BaseScheduler

import settings
from hooks import discord_hook


def enable_job_exception_logging(scheduler: BaseScheduler):
    def listener(event: JobExecutionEvent):
        exception = repr(event.exception)
        traceback = event.traceback.split("\n", 2)[2]
        payload = {
            "content": (
                f"**Encountered an exception in job __{event.job_id}__**"
                f"```{exception}\n{traceback}```"
            )
        }

        discord_hook(settings.DEBUG_DISCORD_HOOK_URL, payload)

    scheduler.add_listener(listener, EVENT_JOB_ERROR)
