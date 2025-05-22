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

Example output (May 21st 2025):
```
Loading cache for FIN metadata
Searching for Ashe in FIN
Found 1 slots between
 #6 colors ['W'], name ambrosia whiteheart
 #8 colors ['W'], name auron's inspiration
Found 2 slots between
 #170 colors ['R'], name zell dincht
 #173 colors ['G'], name balamb t-rexaur
Found 3 slots between
 #251 colors ['R', 'W'], name zidane, tantalus thief
 #255 colors [], name buster sword
Found 2 slots between
 #271 colors [], name adventurer's inn
 #274 colors [], name capital city
Found 242 slots between
 #309 colors [], name wastes
 #552 colors ['R', 'W'], name cloud, planet's champion
```

## Set meta data
Set meta data (from the scryfall api sets endpoint) is being cached currently. The hope was to use it to "cut off" non booster cards, but I don't see a good way of doing so.

## Contributing
* Run all tests (`run_tests.sh`)
* Run formatter (`format.sh` uses `ruff`)