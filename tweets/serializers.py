from tweets.models import Tweet
from rest_framework import serializers

class TweetSerializer(serializers.ModelSerializer):
    tweet_id = serializers.CharField()
    created_at = serializers.DateTimeField()
    text = serializers.CharField()
    retweet_count = serializers.IntegerField()
    handle = serializers.CharField()
    media_type = serializers.CharField(allow_null=True)

    class Meta:
        model = Tweet
        fields = ('tweet_id', 'created_at', 'text', 'retweet_count', 'handle', 'media_type')

    def create(self, validated_data):
        tweet, created = Tweet.objects.update_or_create(
            tweet_id=validated_data.get('tweet_id'),
            defaults=validated_data
        )
        return tweet
