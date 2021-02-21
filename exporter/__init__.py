from prometheus_client.registry import REGISTRY
from prometheus_client import start_http_server
from helpers import global_config, logs
import yaml, logging, asyncio
from pprint import pprint
from .collector import OpenHABCollector

def run():
    REGISTRY.register(OpenHABCollector())

    start_http_server(9876)

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()

