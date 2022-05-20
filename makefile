run_celery:
	celery -A celeryworker.celery worker -l INFO
