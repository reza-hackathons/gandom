#!/bin/bash
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

rm -rf out
rm -f entropy.json

echo "Warming up Golem requestor..."
python3 task_dispatcher.py --min-sources 8 --stream-size 32

python3 aggregator.py

echo "Random streams have been saved to the 'random.json' file."