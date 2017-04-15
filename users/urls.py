from django.conf.urls import url
from users.views import UserView, create_user
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^$', UserView.as_view(), name='user-view'),
    url(r'^create/$', create_user, name='user-create-view'),
    url(r'^api-token-auth/', obtain_jwt_token, name='user-jwt-auth')
]
