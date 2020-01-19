#!/bin/bash
if [ -z "$1" ]
then
	cp config/config_dev.py config/confgi.py
else
	cp config/config_$1.py config/config.py
fi
python3.6 app.py
