# #cebula-bots

## Contributing

To begin, create a new virtual environment, for example using the [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) package. After that, install dependencies:

```bash
$ pip install -r requirements.txt
```

```
.
├── README.md       # This file
├── formatters.py   # Data formatting
├── hooks.py        # Webhooks instructions
├── jobs            # Jobs definition
│   ├── __init__.py # Jobs triggers
│   ├── base.py     # Base structures
│   └── <job_name>.py # Job code
├── main.py         # Scheduler entrypoint
├── retry.py        # Job retry function
├── scheduler.py    # Scheduler intialization
├── settings.py
└── tests
    ├── conftest.py # Fixtures
    └── test_*.py

```

To create a new job, create a new module in `jobs/` directory. After implementing the job, it's definition must be added to `jobs/__init__.py`:

```python
all_jobs = [
    JobDefinition(
        id="xkom", function=xkom, trigger=CronTrigger(hour="10,22", second="10")
    ),
]
```

For triggers documentation, refer to APScheduler's [documentation](https://apscheduler.readthedocs.io/en/latest/py-modindex.html) (`apscheduler.triggers.*` modules).

## Environment variables

For settings, environment variables are used, along with [python-dotenv](https://github.com/theskumar/python-dotenv) package, which loads `.env` file.

## Running tests

For tests, `pytest` package is used in following manner:

```bash
$ python -m pytest
```

## Code guidelines

Code should be formatted using `black` and `isort`. Be sure to run the following before commiting:

```bash
black . && isort -y
```
