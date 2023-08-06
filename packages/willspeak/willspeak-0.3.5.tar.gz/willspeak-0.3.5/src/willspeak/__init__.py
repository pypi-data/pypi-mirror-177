# Standard lib
import threading

# Local
from .conf import Settings

# Event flag to trigger graceful shutdown
inactive_flag = threading.Event()

# Project settings
settings = Settings(
    appname="WillSpeak"
)
