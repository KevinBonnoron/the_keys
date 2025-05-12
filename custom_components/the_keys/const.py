"""Constants for the The Keys integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "the_keys"
MIN_SCAN_INTERVAL = 10
DEFAULT_SCAN_INTERVAL: Final = timedelta(minutes=1).total_seconds()
