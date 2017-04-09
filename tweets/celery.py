from __future__ import absolute_import

from celery import Celery
from tweets import celeryconfig

app = Celery('tweets',
             include=['tweets.tasks'])

app.config_from_object(celeryconfig)

if __name__ == '__main__':
    app.start()