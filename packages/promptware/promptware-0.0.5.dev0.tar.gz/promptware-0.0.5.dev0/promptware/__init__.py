import os

from dotenv import load_dotenv

from promptware.load import install
from promptware.promptware import DataLabConfig

load_dotenv()

os_api_key = os.getenv("OS_API_KEY")
eb_api_key = os.getenv("EB_API_KEY")
eb_username = os.getenv("EB_USERNAME")


__all__ = [
    "DataLabConfig",
    "OpenAIOSConfig",
    "CohereOSConfig",
    "install",
]
