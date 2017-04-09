from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=None, min_length=4, allow_blank=False, trim_whitespace=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=None, min_length=6, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
