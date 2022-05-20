celery_up:
	celery -A celeryworker.celery worker -f logs/celery.log -D -l INFO

celery_stop:
	ps auxww | grep 'celeryworker' | awk '{print $2}' | xargs kill -9

compose_up:
	docker compose -f docker-compose.yaml up -d

compose_stop:
	docker compose -f docker-compose.yaml stop
