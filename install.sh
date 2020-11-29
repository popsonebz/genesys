#!/bin/bash

pip install -r requirements.txt
./db_migration.sh
source ./env.sh
./su.sh
