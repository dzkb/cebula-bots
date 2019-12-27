import os

from dotenv import load_dotenv

load_dotenv()

# Global settings
DEBUG = os.environ.get("DEBUG", False)
SQLALCHEMY_JOB_STORE = os.environ.get("SQLALCHEMY_JOB_STORE", "sqlite:///jobs.sqlite")

# Job-specific settings
XKOM_DISCORD_HOOK_URL = os.environ.get("XKOM_DISCORD_HOOK_URL")
XKOM_DATA_URL = os.environ.get("XKOM_DATA_URL", "https://x-kom.pl")
