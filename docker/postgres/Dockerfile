FROM postgres:17.5

COPY ./docker/postgres/maintenance /usr/local/bin/maintenance
RUN set -eux; \
    install -m 0755 /usr/local/bin/maintenance/* /usr/local/bin/; \
    rm -rf /usr/local/bin/maintenance

RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends cron && \
    rm -rf /var/lib/apt/lists/*

COPY ./docker/postgres/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab

COPY ./docker/postgres/entrypoint-wrapper.sh /usr/local/bin/

COPY ./docker/postgres/start-cron.sh /usr/local/bin/

# RUN chmod +x /usr/local/bin/entrypoint-wrapper.sh

# RUN chmod +x  /usr/local/bin/start-cron.sh

# ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh"]
