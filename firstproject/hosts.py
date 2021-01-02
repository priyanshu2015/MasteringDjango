from django_hosts import patterns, host
from django.contrib import admin
from . import admin_urls

host_patterns = patterns('',
    host(r'www', 'firstapp.urls', name='www'),
    host(r'services', 'seller.urls', name='services'),
    host(r'admin', admin_urls, name='admin'),
)