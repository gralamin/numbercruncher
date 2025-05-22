from util import API_DELAY, get_data_file, is_cached

import time
import requests
import json
import logging

logger = logging.getLogger(__name__)


# All callers should use this
def get_set(set_to_ask):
    if not is_set_cached(set_to_ask):
        logger.info(f"Querying scryfall for {set_to_ask} cards")
        return scryfall_cache_set(set_to_ask)
    logger.info(f"Loading cache for {set_to_ask} metadata")
    return load_cache(set_to_ask)


def load_cache(set_to_ask):
    cached_data_file = get_data_file(set_to_ask)
    with open(cached_data_file, "r") as f:
        return json.load(f)


def scryfall_cache_set(set_to_ask):
    params = {"order": "set", "q": "set:" + set_to_ask}
    address = "https://api.scryfall.com"
    headers = {"User-Agent": "numbercruncher/0.0.1", "Accept": "application/json"}
    time.sleep(API_DELAY)
    response = requests.get(address + "/cards/search", params=params, headers=headers)
    response.raise_for_status()
    result = response.json()
    cards = result["data"]
    while result["has_more"]:
        time.sleep(API_DELAY)
        response = requests.get(result["next_page"], headers=headers)
        response.raise_for_status()
        result = response.json()
        cards.extend(result["data"])

    cached_data_file = get_data_file(set_to_ask)
    with open(cached_data_file, "w") as f:
        json.dump(cards, f)
    return cards


def is_set_cached(set_to_ask):
    cached_data_file = get_data_file(set_to_ask)
    return is_cached(cached_data_file)
