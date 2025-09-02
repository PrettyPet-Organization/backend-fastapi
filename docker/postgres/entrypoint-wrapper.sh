#!/bin/bash

echo "entrypoint-wrapper opened"
start-cron.sh
docker-entrypoint.sh postgres