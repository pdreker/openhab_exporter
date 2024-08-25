import yaml, sys, requests, logging, re
from helpers import global_config, logs
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from pprint import pprint

logger = logging.getLogger('exporter')
logger.setLevel(global_config._LOGLEVEL)
logger.addHandler(logs.ch)

config = None
prefix = ''
exclude_items = None

def read_configfile():
    global prefix, config, exclude_items
    logger.info(f'reading config file from {global_config.CONFIG_FILE}')
    with open(global_config.CONFIG_FILE, 'r') as conffile:
        conffile = yaml.safe_load(conffile)

    config = conffile['config']
    prefix = config['prefix']
    exclude_items = config['items']['exclude']

class OpenHABCollector(object):
    def __init__(self) -> None:
        super().__init__()
        self.metrics = Metrics()
        read_configfile()

    def collect(self):
        logger.debug('Starting collection in custom collector')
        self.metrics.read_metrics()
        yield from self.metrics.collect_metrics()

class Metrics:            
    def __init__(self) -> None:
        logger.debug('Metrics initializing...')
        self.metrics = {}
        
    def collect_metrics(self):
        for metric in self.metrics.keys():
            yield self.metrics[metric]
        
        self.metrics.clear()

    def new_metric(self, metric, name, value):
        if metric not in self.metrics:
            self.metrics[metric] = GaugeMetricFamily(prefix + metric, metric, labels=['item'])
        
        if isinstance(value, str):
            regex = r'\D*(\d+\.{0,1}\d*)\D*'
            value = re.search(regex, value).group(1)
        self.metrics[metric].add_metric([name], float(value))

    def add_metric(self, item):
        tags = [x.lower() for x in item['tags']]
        type = item['type'].lower()
        name = item['name']
        value = item['state']
        if item['type'].lower() != 'group':
            if 'temperature' in tags and type == 'number:temperature':
                logger.debug(f'Generating temperature metric for {item["name"]} as {prefix + "temperature_c"} (value: {value})')
                self.new_metric('temperature_c', name, value)
            elif 'humidity' in tags and type == 'number:dimensionless':
                logger.debug(f'Generating humidity metric for {item["name"]} as {prefix + "humidity_percent"}')
                self.new_metric('humidity_percent', name, value)
            elif 'pressure' in tags and type == 'number:pressure':
                logger.debug(f'Generating pressure metric for {item["name"]} as {prefix + "pressure_hpa"}')
                self.new_metric('pressure_hpa', name, value)
            elif 'valvestate' in tags and type == 'number:dimensionless':
                logger.debug(f'Generating valvestate metric for {item["name"]} as {prefix + "valvestate_percent"}')
                self.new_metric('valvestate_percent', name, value)
            elif 'switch' in tags:
                logger.debug(f'Generating switch state metric for {item["name"]} as {prefix + "switch_state"}')
                self.new_metric('switch_state', name, 1.0 if str(value).lower == 'on' else 0.0)
            elif 'lowbattery' in tags:
                logger.debug(f'Generating LowBat (switch) state metric {item["name"]} as {prefix + "lowbat_state"}')
                self.new_metric('lowbat_state', name, 1.0 if str(value).lower == 'on' else 0.0)
            elif 'colortemperature' in tags:
                logger.debug(f'Generating colortemp metric {item["name"]} as {prefix + "color_temperature_percent"}')
                self.new_metric('colortemp_percent', name, value)
            elif 'light' in tags and type == 'dimmer':
                logger.debug(f'Generating dimmer metric {item["name"]} as {prefix + "dimmer_percent"}')
                self.new_metric('dimmer_percent', name, value)
            elif 'light' in tags and type == 'color':
                logger.debug(f'Generating color metric {item["name"]} as {prefix + "color_HSB"}')
                value_H, value_S, value_B = value.split(',')
                self.new_metric('color_hue', name, value_H)
                self.new_metric('color_saturation', name, value_S)
                self.new_metric('color_brightness', name, value_B)
            elif 'openstate' in tags and type == 'contact':
                logger.debug(f'Generating contact metric {item["name"]} as {prefix + "contact_state"}')
                self.new_metric('contact_state', name, 1.0 if str(value).lower == 'open' else 0.0)
            else:
                logger.debug(f'Uncategorized item {item["name"]}: category: {item["category"]}, type: {item["type"]}, tags: {item["tags"]}, state: {item["state"]}')
        else:
            if item['groupType'] and item['groupType'].lower() == 'switch':
                logger.debug(f'Generating switch state metric for group {item["name"]} as {prefix + "switch_state"}')
                self.new_metric('switch_state', name, 1.0 if str(value).lower == 'on' else 0.0)

    def read_metrics(self):
        item_response = requests.get(global_config.OPENHAB_URL + '/rest/items', verify=False)
        if item_response.status_code != 200:
            logger.critical(f'Error retrieving items from OpenHAB: response code: {item_response.status_code}, message: {item_response.text}')
            sys.exit(1)

        items = item_response.json()
        for item in items:
            if item['name'] not in exclude_items:
                self.add_metric(item)
            else:
                pass
                #logger.debug(f'Excluding item {item["name"]}')

    def create_prom_metric(self):
        pass

class TemperatureMetrics(Metrics):
    def create_prom_metric(self):
        if not len(self.metrics):
            return

        temp_metric = GaugeMetricFamily('openhab_temperature', 'Temperature metrics extracted from OpenHAB', labels=['item'])
        for m in self.metrics:
            temp_metric.add_metric([m['name']], m['value'])
        
        yield temp_metric