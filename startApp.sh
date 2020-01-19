#!/bin/bash
if [ -z "$1" ]
then
  PATH=/home/sameer/litmusblox_cvParser
  ENV=dev
else
  if [ $1 = "dev" ]; then
    PATH=/home/sameer/litmusblox_cvParser
    ENV=dev
  elif [ $1 = "test" ]; then
    PATH=/home/lbtest/cvParserApplication
    ENV=test

  elif [ $1 = "prod" ]; then
    PATH=/home/lbprod/cvParserApplication
    ENV=prod
  fi
fi

$PATH/config/config_$ENV.py $PATH/config/config.py

python3.6 app.py
