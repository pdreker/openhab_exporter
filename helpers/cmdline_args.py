import argparse
from .logs import logger
from . import global_config

parser = argparse.ArgumentParser(description='Exporter for various OpenHAB metrics including item states.')
parser.add_argument('--config', '-c')
parser.add_argument('--openhab-url', dest='ohurl')
parser.add_argument('--generate-config', dest='action', action='store_const', const='gen_config')

arguments = parser.parse_args()

global_config.CONFIG_FILE = arguments.config if arguments.config != None else global_config.CONFIG_FILE
global_config.ACTION = arguments.action if arguments.action != None else global_config.ACTION
global_config.OPENHAB_URL = arguments.ohurl if arguments.ohurl != None else global_config.OPENHAB_URL

logger.info(f'Run mode: {global_config.ACTION}')
logger.info(f'Reading config file {global_config.CONFIG_FILE}')
