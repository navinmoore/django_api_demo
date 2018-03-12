# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # url(r'^snippets/$', views.snippet_list),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^$', views.UserList.as_view()),
    url(r'^api/token/$', views.ObtainExpiringAuthToken.as_view()),


]


urlpatterns = format_suffix_patterns(urlpatterns)