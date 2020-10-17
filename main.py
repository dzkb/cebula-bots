import asyncio

import settings
from scheduler import scheduler

if settings.DEBUG:
    import logging

    logging.basicConfig(
        format=(
            "%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s.%(funcName)s: "
            "%(message)s"
        ),
        datefmt=r"%H:%M:%S",
    )
    logging.getLogger("apscheduler").setLevel(logging.DEBUG)
else:
    logging.getLogger("apscheduler").setLevel(logging.INFO)


def run():
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down. Please wait...")
        scheduler.shutdown(wait=True)
        exit(0)


if __name__ == "__main__":
    run()
