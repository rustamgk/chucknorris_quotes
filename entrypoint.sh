#!/usr/bin/env sh
set -eu
set -x

PORT=${PORT:-8080}

export FLASK_APP=chucknorris_webapp
exec gunicorn \
  --bind="0.0.0.0:${PORT}" \
  --workers=4 \
  --log-level=info --capture-output \
  "${FLASK_APP}:create_app()"
