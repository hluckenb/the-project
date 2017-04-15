from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=None, min_length=4, allow_blank=False, trim_whitespace=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=None, min_length=6, allow_blank=False, trim_whitespace=True)
    confirm_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'confirm_password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def validate(self, data):
        if self.initial_data['password'] != self.initial_data['confirm_password']:
            raise serializers.ValidationError({
                'password': 'Password and confirmation must match.'
            })
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
