import logging
CONFIG_FILE = './openhab-exporter.yaml'
PORT = 9791
ACTION = 'run_exporter'

OPENHAB_URL = 'https://localhost:8443'

LOGLEVEL = 'INFO'
LOGLEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
_LOGLEVEL = LOGLEVEL_MAP[LOGLEVEL]