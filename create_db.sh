#!/bin/bash

# Install homebrew, if not present
if ! which brew > /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi

if ! brew ls --versions sqlite3 > /dev/null; then
    brew install sqlite3
fi

if ! brew ls --versions pcre > /dev/null; then
    brew install pcre
fi

SQLITE=$(brew --prefix sqlite3)
PCRE=$(brew --prefix pcre)

if [[ ! -f pcre.so ]]; then
    clang -shared -o pcre.so -L$SQLITE/lib -L$PCRE/lib -lsqlite3 -lpcre -Werror pcre.c -I$SQLITE/include -I$PCRE/include -fPIC
fi

# Convert JSON to CSV for import
python3 << EOF
import csv, json

with open('data.json') as jsonfile:
    data = json.load(jsonfile)

    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writerows(data)
EOF

# Create table, if needed. Import data
$SQLITE/bin/sqlite3 data.db << EOF
.load $(pwd)/pcre.so

CREATE TABLE IF NOT EXISTS commodities (
    country TEXT NOT NULL CHECK(LENGTH(country) == 2),
    commodity TEXT NOT NULL,
    fixed_overhead TEXT NOT NULL CHECK(fixed_overhead REGEXP '^\d+(\.?\d+)?$'),
    variable_cost TEXT NOT NULL CHECK(variable_cost REGEXP '^\d+(\.?\d+)?$') 
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_commodities_country_commodity ON commodities (country, commodity);

.mode csv
.import data.csv commodities
EOF
