#!/bin/bash
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

if [ $# -lt 3 ]
then
    echo "USAGE: './script.sh -s 8 -l 16' -s: min sources, -l: stream size"
fi

while getopts ":s:l:" opt; do
  case $opt in
    s) min_sources="$OPTARG"
    ;;
    l) length="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

rm -rf out random.json

echo "Warming up Golem requestor for $min_sources sources and $length random bytes."

python3 task_dispatcher.py --min-sources $min_sources --stream-size $length

python3 aggregator.py

echo "Random streams have been saved to the 'random.json' file."