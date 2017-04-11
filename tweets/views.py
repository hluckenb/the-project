from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncHour, TruncDay
from django.db.models import Count, Max
from tweets import serializers
from tweets.models import Tweet
from tweets.serializers import TweetSerializer

class TweetView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        tweets_by_hour = Tweet.objects \
            .annotate(hour=TruncHour('created_at')) \
            .values('hour').annotate(count=Count('id')) \
            .values('hour', 'count').order_by('hour')

        most_retweeted = Tweet.objects.raw('select distinct on (date(created_at)) retweet_count, * from tweets_tweet order by date(created_at), retweet_count desc;')
        most_retweeted_by_day = []
        for record in most_retweeted:
            most_retweeted_by_day.append(TweetSerializer(record).data)

        return Response({ 'tweets_by_hour': tweets_by_hour, 'most_retweeted_by_day': most_retweeted_by_day })
