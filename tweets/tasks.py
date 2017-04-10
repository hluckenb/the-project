from __future__ import absolute_import

import os
import base64
import requests

from django.core.cache import cache
from tweets.celery import app
from urllib.parse import parse_qs

@app.task
def start_collection(hashtag='radiohead')
    get_tweets(f'?q=%23{hashtag}')

@app.task
def get_tweets(query):
    r = requests.get(f'https://api.twitter.com/1.1/search/tweets.json{query}', headers={'Authorization': 'Bearer ' + token()})

    next_query = r.json()['search_metadata']['next_results']
    if next_query:
        get_tweets.delay(next_query)

    return r.json()

def token():
    token = cache.get('access-token')

    if token is None:
        token = get_token()
        cache.set('access-token', token, None)

    return token

def get_token():
    auth_data = encode(os.environ.get('TWITTER_CONSUMER_KEY') + ':' + os.environ.get('TWITTER_CONSUMER_SECRET'))

    r = requests.post('https://api.twitter.com/oauth2/token', headers={'Authorization': f'Basic {auth_encoded}'}, data={'grant_type': 'client_credentials'})
    return r.json()['access_token']

def encode(val):
    return base64.b64encode(bytes(val, encoding='utf-8')).decode('utf-8')

# from tweets.tasks import get_tweets