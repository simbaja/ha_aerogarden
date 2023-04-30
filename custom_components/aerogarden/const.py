from datetime import timedelta

DOMAIN = "aerogarden"
SENSOR_PREFIX = "aerogarden"
DEFAULT_HOST = "https://app3.aerogarden.com:8443"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

VALUES_SCAN_INTERVAL = [30, 60, 120, 300, 600]
DEFAULT_SCAN_INTERVAL = VALUES_SCAN_INTERVAL[2]