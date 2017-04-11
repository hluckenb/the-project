from django.conf.urls import url
from tweets.views import TweetView

urlpatterns = [
    url(r'^$', TweetView.as_view(), name='tweet-view'),
]
