#!/bin/bash

set -euo pipefail

# If we are in a development environment, execute the pre-start script
if [ "$ENVIRONMENT" == "dev" ]; then
    source pre-start.sh
fi

uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
