#!/bin/bash
# ShravScript language runner for Unix-like systems

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 not found. Please install Python 3.6 or higher."
    exit 1
fi

# Get the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Run the ShravScript interpreter with all arguments
python3 "$SCRIPT_DIR/src/main.py" "$@" 