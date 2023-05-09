"""Constants for the The Keys integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "the_keys"
DEFAULT_SCAN_INTERVAL: Final = timedelta(minutes=11)
MIN_SCAN_INTERVAL: Final = 60
