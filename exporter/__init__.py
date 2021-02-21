from prometheus_client.registry import REGISTRY
from prometheus_client import start_http_server
from helpers import global_config, logs
import yaml, logging, asyncio
from pprint import pprint
from .collector import OpenHABCollector

logger = logging.getLogger('collector')
logger.setLevel(global_config._LOGLEVEL)
logger.addHandler(logs.ch)

def run():
    REGISTRY.register(OpenHABCollector())

    logger.info(f'Starting webserver on port {global_config.PORT}...')
    start_http_server(global_config.PORT)

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()

