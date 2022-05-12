#!/bin/bash

set -euo pipefail

ENV_FILE="${PWD}/.env-dev"

if [ -f ${ENV_FILE} ]
then
  export $(cat ${ENV_FILE} | xargs)
fi

poetry run uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
