#!/bin/bash

cp ./.env.$1 ./.env
python3.6 app.py