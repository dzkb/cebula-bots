from apscheduler.triggers.cron import CronTrigger

from jobs.base import JobDefinition
from jobs.morele import run as morele
from jobs.xkom import run as xkom

all_jobs = [
    JobDefinition(
        id="xkom", function=xkom, trigger=CronTrigger(hour="10,22", second="10")
    ),
    JobDefinition(id="morele", function=morele, trigger=None),
]
