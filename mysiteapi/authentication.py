# -*- coding:utf-8 -*-
import datetime
import pytz

from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        print 'key', key
        cache_user = cache.get(key)
        print 'cache_user', cache_user
        if cache_user:
            return (cache_user, key)

        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        time_now = datetime.datetime.now()
        utc = pytz.UTC
        if token.created < utc.localize(time_now - datetime.timedelta(minutes=EXPIRE_MINUTES)):
            token.delete()
            raise exceptions.AuthenticationFailed(_('Token has expired then delete'))
        else:
            print 'token update'
            token.created = time_now
            token.save()

        if token:
            print 'i am here'
            cache.set(key, token.user, EXPIRE_MINUTES*6)
        return (token.user, token)