"""get_request URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import get_request.views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', get_request.views.index),
    url(r'^info$', get_request.views.info),
    url(r'^domain_status$', get_request.views.get_status),
    url(r'^domain_ip$', get_request.views.get_ip),
    url(r'^ip$', get_request.views.ip),
    url(r'^get$', get_request.views.get),
    url(r'^bitcoin$', get_request.views.address),
    url(r'^server-location$', get_request.views.server_info),
    url(r'^company-contact$', get_request.views.company_information),
    url(r'^twitter$', get_request.views.twitter_search),
    url(r'^ssl-cert$', get_request.views.get_ssl),
    url(r'^ssl$', get_request.views.get_ssl_source),
    url(r'^blacklist$', get_request.views.get_blacklist),
    url(r'^ping$', get_request.views.ping),
]
