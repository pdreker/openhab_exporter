import logging
from helpers import global_config

# create logger
logger = logging.getLogger('openhab_exporter')
logger.setLevel(global_config._LOGLEVEL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(global_config._LOGLEVEL)

# create formatter
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
