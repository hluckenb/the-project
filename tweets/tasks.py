from __future__ import absolute_import

import os
import time
import base64
import requests

from django.core.cache import cache
from urllib.parse import parse_qs
from tweets.celery import app
from tweets.serializers import TweetSerializer

def start_collection(hashtag='radiohead'):
    get_tweets.delay(f'?q=%23{hashtag}')

@app.task
def get_tweets(query):
    r = requests.get(f'https://api.twitter.com/1.1/search/tweets.json{query}', headers={'Authorization': 'Bearer ' + token()})

    for status in r.json().get('statuses'):
        serializer = TweetSerializer(data=parse(status))
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

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

def parse(data):
    return {
             'tweet_id' : data.get('id'),
           'created_at' : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.strptime(data.get('created_at'), '%a %b %d %H:%M:%S +0000 %Y')),
                 'text' : data.get('text'),
        'retweet_count' : data.get('retweet_count'),
               'handle' : data.get('user').get('screen_name'),
           'media_type' : media_type(data.get('entities').get('media'))
    }

def media_type(media):
    return media[0].get('type') if media else None
