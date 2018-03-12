# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserRegisterSerializer(serializers.Serializer):

    def create(self, validated_data):
        print 'haha', validated_data
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', "password", "email", "is_staff")


