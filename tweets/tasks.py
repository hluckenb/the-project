from __future__ import absolute_import

import os
import pytz
import base64
import requests

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from urllib.parse import parse_qs
from tweets.celery import app
from tweets.serializers import TweetSerializer

@app.task
def start_collection(hashtag='radiohead', days=7):
    days_ago = datetime.now(pytz.timezone(settings.TIME_ZONE)) - timedelta(days=days)
    twitter_format = days_ago.strftime('%Y-%m-%d')
    get_tweets.delay('?q=%23' + hashtag + '%20since:' + twitter_format + '%20exclude:replies%20exclude:retweets%20lang:en&count=100')

@app.task
def get_tweets(query):
    r = api_request().get('https://api.twitter.com/1.1/search/tweets.json' + query,
        headers={'Authorization': 'Bearer ' + token()}
    )

    for status in r.json().get('statuses'):
        serializer = TweetSerializer(data=parse(status))
        if serializer.is_valid():
            serializer.save()

    next_query = r.json().get('search_metadata').get('next_results')
    if next_query:
        get_tweets.delay(next_query)

def token():
    token = cache.get('access-token')

    if token is None:
        token = get_token()
        cache.set('access-token', token, None)

    return token

def get_token():
    auth_data = encode(os.environ.get('TWITTER_CONSUMER_KEY') + ':' + os.environ.get('TWITTER_CONSUMER_SECRET'))

    r = api_request().post('https://api.twitter.com/oauth2/token',
        headers={'Authorization': 'Basic ' + auth_data},
        data={'grant_type': 'client_credentials'}
    )

    return r.json().get('access_token')

def encode(val):
    return base64.b64encode(bytes(val, encoding='utf-8')).decode('utf-8')

def parse(data):
    created_at = datetime.strptime(data.get('created_at'), '%a %b %d %H:%M:%S +0000 %Y')

    return {
             'tweet_id' : data.get('id_str'),
           'created_at' : pytz.utc.localize(created_at),
                 'text' : data.get('text'),
        'retweet_count' : data.get('retweet_count'),
               'handle' : data.get('user').get('screen_name'),
           'media_type' : media_type(data.get('entities').get('media'))
    }

def media_type(media):
    return media[0].get('type') if media else None

def api_request():
    session = requests.Session()

    retries = Retry(total=5,
        backoff_factor=60,
        status_forcelist=[500, 502, 503, 504]
    )

    session.mount('https://', HTTPAdapter(max_retries=retries))

    return session
