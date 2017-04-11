from django.db import models

class Tweet(models.Model):

    tweet_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    text = models.TextField()
    retweet_count = models.IntegerField()
    handle = models.CharField(max_length=255)
    media_type = models.CharField(null=True, max_length=255)

    collected_at = models.DateField(auto_now_add=True)
