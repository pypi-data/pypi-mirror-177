import os

import slack_sdk
from dotenv import load_dotenv

from .config import edit_conf, is_env_available, is_env_outdated
from .help import help

__version__ = "0.2.3"

if not is_env_available():
    print("WARNING: Config parameters are not set.")
    edit_conf()
if is_env_outdated():
    print("WARNING: Config parameters are outdated.")
    edit_conf()

load_dotenv(dotenv_path=os.path.dirname(os.path.realpath(__file__)) + "/.env")

# Slack client initialized.
client = slack_sdk.WebClient(token=os.getenv("SLACK_TOKEN"))

from .message import send_message
from .notifications import start_notif, end_notif
from .reminder_message import *
from .timed_message import *
