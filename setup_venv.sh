#!/bin/bash

# Install homebrew, if not present
if ! which brew > /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi

if ! brew ls --versions python@3.8 > /dev/null; then
    brew install python@3.8
fi

PYTHON=$(brew --prefix python@3.8)/bin/python3

$PYTHON -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt