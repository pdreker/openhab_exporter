import argparse
from .logs import logger
from . import global_config

parser = argparse.ArgumentParser(description='Exporter for various OpenHAB metrics including item states.')
parser.add_argument('--config', '-c')
parser.add_argument('--port', '-p')
parser.add_argument('--openhab-url', dest='ohurl')
parser.add_argument('--generate-config', dest='action', action='store_const', const='gen_config')
parser.add_argument('--log-level', dest='loglevel', choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'])


arguments = parser.parse_args()

global_config.CONFIG_FILE = arguments.config if arguments.config != None else global_config.CONFIG_FILE
global_config.PORT = arguments.port if arguments.port else global_config.PORT
global_config.ACTION = arguments.action if arguments.action != None else global_config.ACTION
global_config.OPENHAB_URL = arguments.ohurl if arguments.ohurl != None else global_config.OPENHAB_URL
global_config.LOGLEVEL = arguments.loglevel if arguments.loglevel else global_config.LOGLEVEL



logger.info(f'Run mode: {global_config.ACTION}')
logger.info(f'Config file: {global_config.CONFIG_FILE}')
logger.info(f'Port: {global_config.PORT}')
logger.info(f'Log level: {global_config.LOGLEVEL}')
logger.info(f'OpenHAB URL: {global_config.OPENHAB_URL}')
