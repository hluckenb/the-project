from tweets.models import Tweet
from rest_framework import serializers

class TweetSerializer(serializers.ModelSerializer):
    tweet_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    text = serializers.CharField()
    retweet_count = serializers.IntegerField()
    handle = serializers.CharField()
    media_type = serializers.CharField(allow_null=True)

    class Meta:
        model = Tweet
        fields = ('tweet_id', 'created_at', 'text', 'retweet_count', 'handle', 'media_type')

    def create(self, validated_data):
        return Tweet.objects.create(**validated_data)
