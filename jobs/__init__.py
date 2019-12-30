from datetime import datetime

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from pytz import utc

from jobs.base import JobDefinition
from jobs.morele import run as morele
from jobs.xkom import run as xkom

all_jobs = [
    JobDefinition(
        id="xkom",
        function=xkom,
        trigger=CronTrigger(hour="10,22", minute="0", second="10"),
    ),
    JobDefinition(
        id="morele",
        function=morele,
        trigger=IntervalTrigger(
            start_date=datetime(2019, 12, 27, 14, 0, tzinfo=utc), days=3, timezone=utc
        ),
    ),
]
