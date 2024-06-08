from .celery import app as celery_app

#to make sure celery recognises correct app 

__all__ = ['celery_app',]