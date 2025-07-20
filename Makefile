.PHONY: \
install-base \
install-full \
typecheck-basedpyright \
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

typecheck-basedpyright:
	uv run --no-sync basedpyright

format-code:
	uv run --no-sync autoflake .
	uv run --no-sync ruff check --fix --show-fixes
	-uv run --no-sync ruff format --diff
	uv run --no-sync ruff format

run:
	uv run --no-sync src/main.py

makemigrations:
	uv run alembic -c src/alembic.ini revision --autogenerate -m "${msg}"

migrate:
	uv run alembic -c src/alembic.ini upgrade head

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

docker-postgres-create-backup:
	 docker-compose -f docker-compose.yml --env-file .env exec backend-fastapi-postgres backup

docker-postgres-restore:
	cp ./restore.sql.gz ./backups
	docker-compose -f docker-compose.yml --env-file .env exec backend-fastapi-postgres restore restore.sql.gz
	rm ./backups/restore.sql.gz
