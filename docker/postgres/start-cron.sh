#!/bin/bash

if [ "${CRON_PATH}" ]; then
    rm -rf /etc/cron.d
    ln -sfTv "${CRON_PATH}" /etc/cron.d
fi

chmod -R go-w /etc/cron.d

env | while read -r line; do
    IFS="=" read var val <<< ${line}
    sed --in-place "/^${var}[[:blank:]=]/d" /etc/security/pam_env.conf || true
    echo "${var} DEFAULT=\"${val}\"" >> /etc/security/pam_env.conf
done

service cron start

trap "service cron stop; kill \$!; exit" SIGINT SIGTERM