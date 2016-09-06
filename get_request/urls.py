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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^info$', get_request.views.info),
    url(r'^get_status$', get_request.views.get_status),
    url(r'^get_ip$', get_request.views.get_ip),
    url(r'^ip$', get_request.views.ip),
    url(r'^get$', get_request.views.get),
    url(r'^bitcoin$', get_request.views.address),
    url(r'^ipinfo$', get_request.views.ip_info),
    url(r'^machine-payable$', get_request.views.machine_payable),
]
