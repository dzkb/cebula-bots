import os

from dotenv import load_dotenv

load_dotenv()

# Global settings
DEBUG = os.environ.get("DEBUG", False)
DEBUG_DISCORD_HOOK_URL = os.environ.get("DEBUG_DISCORD_HOOK_URL")
SQLALCHEMY_JOB_STORE = os.environ.get("SQLALCHEMY_JOB_STORE", "sqlite:///jobs.sqlite")

# Job retry settings
JOB_RETRY_DELAY = int(os.environ.get("JOB_RETRY_DELAY", "5"))
JOB_MAX_RETRIES = int(os.environ.get("JOB_MAX_RETRIES", "5"))

# Job-specific settings
XKOM_DISCORD_HOOK_URL = os.environ.get("XKOM_DISCORD_HOOK_URL")

MORELE_DISCORD_HOOK_URL = os.environ.get("MORELE_DISCORD_HOOK_URL")

PROLINE_DISCORD_HOOK_URL = os.environ.get("PROLINE_DISCORD_HOOK_URL")
