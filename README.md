# MTG Scryfall Number Cruncher
Queries the scryfall API to get number crunched data. Caches data every 12 hours during spoiler season.

## Installation
Requires python. Create a virtualenv, and activate it:
```
python3 -m venv venv
source venv/bin/activate
```

Then install requests:
```
pip install requests
```

## Running
Use the python in `venv/bin/python` on `main.py` to run the script
```
venv/bin/python main.py -s FIN -c Ashe
```

## Set meta data
Set meta data (from the scryfall api sets endpoint) is being cached currently. The hope was to use it to "cut off" non booster cards, but I don't see a good way of doing so.

## Contributing
* Run all tests (`run_tests.sh`)
* Run formatter (`format.sh` uses `ruff`)