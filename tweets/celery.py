from __future__ import absolute_import

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the-project.settings')

import django
django.setup()

from celery import Celery
from tweets import celeryconfig

app = Celery('tweets', include=['tweets.tasks'])

app.config_from_object(celeryconfig)

if __name__ == '__main__':
    app.start()
