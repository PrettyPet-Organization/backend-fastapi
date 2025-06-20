.PHONY: \
install-base \
install-full \
typecheck-mypy \
typecheck-pyright \
format-code \
run \
makemigrations \
migrate \
docker-run \
docker-run-build \
docker-reload \
docker-reload-build \
docker-down \
docker-logs \
docker-postgres-logs

install-base:
	uv sync --no-dev

install-full:
	uv sync --all-groups

typecheck-mypy:
	uv run --no-sync mypy .

typecheck-pyright:
	uv run --no-sync pyright

format-code:
	uv run --no-sync autoflake .
	uv run --no-sync ruff check --fix --show-fixes
	-uv run --no-sync ruff format --diff
	uv run --no-sync ruff format

run:
	uv run --no-sync src/main.py

makemigrations:
	cd src && uv run alembic revision --autogenerate -m "${msg}"

migrate:
	cd src && uv run alembic upgrade head

docker-run:
	docker compose up -d

docker-run-build:
	docker compose up -d --build

docker-reload:
	sh -c "docker compose down && docker compose up -d" 

docker-reload-build:
	sh -c "docker compose down && docker compose up -d --build"

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f backend-fastapi

docker-postgres-logs:
	docker compose logs -f backend-fastapi-postgres
