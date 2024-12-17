from celery import Celery
from src.api.app import app

def make_celery(app):
    celery = Celery(
        "test_api_celery",
        backend='redis://localhost:6379/0',  # Используй Redis как бэкенд
        broker='redis://localhost:6379/0'    # И тоже Redis для брокера
    )
    return celery


celery = make_celery(app)
