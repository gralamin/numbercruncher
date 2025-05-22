from util import API_DELAY, get_data_file, is_cached

import time
import requests
import json
import logging

logger = logging.getLogger(__name__)


# All callers should use this
def get_set_metadata(set_to_ask):
    if not is_set_meta_cached(set_to_ask):
        logger.info(f"Querying scryfall for {set_to_ask} metadata")
        return scryfall_cache_set_metadata(set_to_ask)
    logger.info(f"Loading cache for {set_to_ask} metadata")
    return load_cache_metadata(set_to_ask)


def load_cache_metadata(set_to_ask):
    cached_data_file = get_data_file(set_to_ask, meta=True)
    with open(cached_data_file, "r") as f:
        return json.load(f)


def scryfall_cache_set_metadata(set_to_ask):
    time.sleep(API_DELAY)
    address = "https://api.scryfall.com"
    headers = {"User-Agent": "numbercruncher/0.0.1", "Accept": "application/json"}
    response = requests.get(address + "/sets/" + set_to_ask, headers=headers)
    response.raise_for_status()
    result = response.json()

    cached_data_file = get_data_file(set_to_ask, meta=True)
    with open(cached_data_file, "w") as f:
        json.dump(result, f)
    return result


def is_set_meta_cached(set_to_ask):
    cached_data_file = get_data_file(set_to_ask, meta=True)
    return is_cached(cached_data_file)
