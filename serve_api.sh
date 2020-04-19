#!/bin/bash

# Handle any missing dependencies then run uvicorn

if [[ ! -f data.db ]]; then
    ./create_db.sh
fi

if [[ ! -f pcre.so ]]; then
    clang -shared -o pcre.so -L/usr/local/lib -lsqlite3 -lpcre -Werror pcre.c -I/usr/local/include
fi

if [[ ! -f .venv/bin/activate ]]; then
    ./setup_venv.sh
fi    
source .venv/bin/activate

uvicorn fruitpal:app $@