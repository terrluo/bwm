run_celery:
	celery -A celeryworker.celery worker -f logs/celery.log -D -l INFO

compose_up:
	docker compose -f docker-compose.yaml up -d

compose_stop:
	docker compose -f docker-compose.yaml stop
