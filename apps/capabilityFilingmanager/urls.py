# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*capabilityFilinglist\.html', views.capabilityFilinglist, name='capabilityFilinglist'),
    url(r'^.*create$', views.create),
    url(r'^.*delete$', views.delete),
    url(r'^.*reportdata', views.reportdata),
    url(r'^.*capabilityFilingdata', views.capabilityFilingdata),
    url(r'^.*capabilityFilingform\.html', views.capabilityFilingform),
    url(r'^.*template$', views.template_download),
    # The home page
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'^$', views.index, name='index'),
]
