import requests, logging, sys, yaml
from helpers import global_config, logs

logger = logging.getLogger('generate_config')

def run():
    item_response = requests.get(global_config.OPENHAB_URL + '/rest/items', verify=False)
    if item_response.status_code != 200:
        logger.critical(f'Error retrieving items from OpenHAB: response code: {item_response.status_code}, message: {item_response.text}')
        sys.exit(1)
    
    items = [ x['name'] for x in item_response.json() ]
    config =  { 'config': {'items': { 'include': sorted(items, key=str.lower) }}}
    print(yaml.dump(config))    

