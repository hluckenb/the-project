import pytz

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncHour, TruncDay
from django.db.models import Count, Max
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from tweets.models import Tweet
from tweets.serializers import TweetSerializer

class TweetView(APIView):

    def get(self, request, format=None):
        week_previous = timezone.now() - timedelta(days=7)

        tweets_by_hour = Tweet.objects.filter(created_at__gte=week_previous) \
            .annotate(hour=TruncHour('created_at')) \
            .values('hour').annotate(count=Count('id')) \
            .values('hour', 'count').order_by('hour')

        most_retweeted = Tweet.objects.raw("""
            select distinct on (date(created_at at time zone 'US/Central')) *
            from tweets_tweet where created_at > NOW() - INTERVAL '7 days'
            order by (date(created_at at time zone 'US/Central')), retweet_count desc;
        """)
        most_retweeted_by_day = []
        for record in most_retweeted:
            most_retweeted_by_day.append(TweetSerializer(record).data)

        return Response({ 'tweets_by_hour': tweets_by_hour, 'most_retweeted_by_day': most_retweeted_by_day })
