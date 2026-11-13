# Multiplayer Game Server Manager

Python 3 standard-library TCP health monitor for game services. Performs connection checks, stores timestamped JSON Lines history, and exports a JSON summary. TCP connectivity **does not** prove game protocol health.

## Try it locally
Terminal 1: `python demo_server.py --port 8765`

Terminal 2: `python server_manager.py --config servers.json --once`

Repeat checks with `python server_manager.py --config servers.json --interval 10 --count 5`. Output is written to `output/` (ignored by Git).

## Tests
`python -m unittest discover -s tests -v`

Only monitor servers you own or are authorized to check. The example config uses loopback only.
