#!/bin/bash

# Handle any missing dependencies then run uvicorn

if [[ ! -f data.db ]]; then
    ./create_db.sh
fi

SQLITE=$(brew --prefix sqlite3)
PCRE=$(brew --prefix pcre)

if [[ ! -f pcre.so ]]; then
    clang -shared -o pcre.so -L$SQLITE/lib -L$PCRE/lib -lsqlite3 -lpcre -Werror pcre.c -I$SQLITE/include -I$PCRE/include -fPIC
fi

if [[ ! -f .venv/bin/activate ]]; then
    ./setup_venv.sh
fi    
source .venv/bin/activate

uvicorn fruitpal:app $@
