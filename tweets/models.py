from django.db import models

class Tweet(models.Model):

    tweet_id = models.BigIntegerField
    tweet_created_at = models.DateField
    text = models.TextField
    retweet_count = models.IntegerField
    by = models.CharField

    created_at = models.DateField(auto_now_add=True)