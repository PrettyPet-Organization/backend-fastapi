FROM python:3.13-slim

WORKDIR /backend-fastapi

ENV PATH="/root/.cargo/bin:${PATH}"
ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY Makefile Makefile
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN make install-base

COPY ./src ./src

CMD ["sh", "-c", "export DOTENV_MODE=true && uv add python-dotenv && make run"]
