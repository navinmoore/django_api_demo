# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import pytz

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics

from .serializers import UserRegisterSerializer

from mysiteapi import settings
from mysiteapi import authentication


EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        serializer.save(
            username = self.request.data.get('username'),
            password = self.request.data.get('password'),
            email = self.request.data.get('email'),
            is_staff = 1
        )


class ObtainExpiringAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            time_now = datetime.datetime.now()
            print type(token.created), token.created
            print type(time_now - datetime.timedelta(minutes=EXPIRE_MINUTES)), time_now - datetime.timedelta(minutes=EXPIRE_MINUTES)
            utc = pytz.UTC
            if created or token.created < utc.localize(time_now - datetime.timedelta(minutes=EXPIRE_MINUTES)):
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = time_now
                token.save()
            print token.key
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





