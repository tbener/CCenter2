'''
Created on Jun 30, 2016

@author: TBENER
'''

from django.conf.urls import url

from . import views

app_name = 'ccenter'

urlpatterns = [
    # ex: /test/
    url(r'^$', views.test, name='test'),
    # ex: /page/5/
    url(r'^(?P<page_id>[0-9]+)/$', views.page, name='page'),
]