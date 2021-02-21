import logging, json, argparse, yaml
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

from helpers import global_config, logs
import config_generator
import exporter

logger = logging.getLogger('openhab_exporter')

def main():
    import helpers.cmdline_args # pylint: disable=unused-import
    
    if global_config.ACTION == 'gen_config':
        config_generator.run()

    elif global_config.ACTION == 'run_exporter':
        exporter.run()

if __name__ == '__main__':
    main()