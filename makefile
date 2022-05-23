celery-up:
	celery -A celeryworker.celery worker -f logs/celery.log -D -l INFO

celery-stop:
	ps auxww | grep 'celeryworker' | awk '{print $2}' | xargs kill -9

compose-up:
	docker compose -f docker-compose.yaml up -d

compose-stop:
	docker compose -f docker-compose.yaml stop

install:
	poetry shell
	poetry install --no-root

pcu:
	pre-commit autoupdate
