#!/bin/bash

MIN_PYTHON_MAJOR_VERSION=3
MIN_PYTHON_MINOR_VERSION=8

# Check if Python is installed and meets the minimum version requirement
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f2)

# Compare the Python version with the minimum required version
if [ $PYTHON_MAJOR_VERSION -lt $MIN_PYTHON_MAJOR_VERSION ]; then
    echo "Python is not installed or does not meet the minimum version requirement. Exiting"
    exit 1
elif [ $PYTHON_MAJOR_VERSION -eq $MIN_PYTHON_MAJOR_VERSION ] && [ $PYTHON_MINOR_VERSION -lt $MIN_PYTHON_MINOR_VERSION ]; then
    echo "Python is installed, but the version is below the required minimum version of $MIN_PYTHON_MAJOR_VERSION.$MIN_PYTHON_MINOR_VERSION. Exiting"
    exit 1
else
    echo "Python $MIN_PYTHON_MAJOR_VERSION.$MIN_PYTHON_MINOR_VERSION or higher is installed."
fi

# Create a virtual environment and install the required packages
if [ -d "venv" ]; then
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create a Token.json file and write {}
echo "{}" > Token.json

echo "Installation completed, run start.sh to start the bot"
