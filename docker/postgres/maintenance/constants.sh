#!/bin/bash

if [ -z "${TZ-}" ]; then
  TZ="UTC"
fi

if [ -z "${PG_BACKUPS_RETENTION_DAYS-}" ]; then
  PG_BACKUPS_RETENTION_DAYS=7
fi

BACKUP_DIR_PATH='/backups'
BACKUP_FILE_PREFIX='backup'
