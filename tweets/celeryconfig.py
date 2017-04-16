from __future__ import absolute_import

from celery.schedules import crontab

BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'rpc://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'US/Central'
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {
    'hourly-collection': {
        'task': 'tweets.tasks.start_collection',
        'schedule': crontab(minute=0, hour='*'),
        'args': ()
    }
}