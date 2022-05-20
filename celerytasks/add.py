from bwm import celery


@celery.task()
def add_together(a, b):
    print("run add_together function")
    return a + b
