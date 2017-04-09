from django.conf.urls import url
from users.views import UserView, create_user

urlpatterns = [
    url(r'^$', UserView.as_view(), name='user-view'),
    url(r'^create/$', create_user, name='user-create-view'),
]
