from celery import Celery
from flask import current_app as app

def make_celery(app):
    celery = Celery(
        app.name,
        backend = app.config['CELERY_RESULT_BACKEND'],
        broker = app.config['CELERY_BROKER_URL'],
        enable_utc = app.config['CELERY_ENABLE_UTC'],
        timezone = app.config['CELERY_TIMEZONE'],
        

    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery