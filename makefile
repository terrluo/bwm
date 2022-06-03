celery-up:
	poetry run celery -A celeryworker.celery worker -f logs/celery.log -D -l INFO

celery-stop:
	ps auxww | grep 'celeryworker' | awk '{print $2}' | xargs kill -9

compose-pull:
ifeq ($(ENV),)
	docker compose -f docker-compose.yaml pull
else
	docker compose -f docker-compose.$(ENV).yaml pull
endif

compose-up:
ifeq ($(ENV),)
	docker compose -f docker-compose.yaml up -d
else
	docker compose -f docker-compose.$(ENV).yaml up -d
endif

compose-stop:
ifeq ($(ENV),)
	docker compose -f docker-compose.yaml stop
else
	docker compose -f docker-compose.$(ENV).yaml stop
endif

install:
	poetry shell
	poetry install --no-root

db-upgrade:
	poetry run flask db upgrade

test:
	poetry run pytest

pcu:
	pre-commit autoupdate
