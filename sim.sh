#!/bin/bash

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change directory to the script directory
cd "$SCRIPT_DIR"

# Execute the Python script
python bottie_exp/sim/simulator.py
