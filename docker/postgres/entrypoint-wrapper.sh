#!/bin/bash

echo "entrypoint-wrapper opened"
start-cron.sh
exec docker-entrypoint.sh postgres -c listen_addresses='*' "$@"