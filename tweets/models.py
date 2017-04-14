from django.db import models

class Tweet(models.Model):

    tweet_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    text = models.TextField()
    retweet_count = models.IntegerField(db_index=True)
    handle = models.CharField(max_length=255)
    media_type = models.CharField(null=True, max_length=255, db_index=True)

    collected_at = models.DateTimeField(auto_now_add=True)
