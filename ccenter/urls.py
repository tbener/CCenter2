'''
Created on Jun 30, 2016

@author: TBENER
'''

from django.conf.urls import url

from . import views

app_name = 'ccenter'

urlpatterns = [
    url(r'^(?P<folder_id>[0-9]+)/(?P<page_id>[0-9]+)/$', views.page, name='folder-page'),
    url(r'^(?P<page_id>[0-9]+)/$', views.page, name='page'),
    url(r'^', views.home, name='home'),
]