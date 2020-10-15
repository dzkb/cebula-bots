import os

from dotenv import load_dotenv

load_dotenv()

# Global settings
DEBUG = os.environ.get("DEBUG", False)
SQLALCHEMY_JOB_STORE = os.environ.get("SQLALCHEMY_JOB_STORE", "sqlite:///jobs.sqlite")

# Job retry settings
JOB_RETRY_DELAY = int(os.environ.get("JOB_RETRY_DELAY", "5"))
JOB_MAX_RETRIES = int(os.environ.get("JOB_MAX_RETRIES", "5"))

# Job-specific settings
XKOM_DISCORD_HOOK_URL = os.environ.get("XKOM_DISCORD_HOOK_URL")
XKOM_RETRY_DELAY_SECS = int(os.environ.get("XKOM_RETRY_DELAY_SECS", "60"))

MORELE_DISCORD_HOOK_URL = os.environ.get("MORELE_DISCORD_HOOK_URL")

PROLINE_DISCORD_HOOK_URL = os.environ.get("PROLINE_DISCORD_HOOK_URL")
