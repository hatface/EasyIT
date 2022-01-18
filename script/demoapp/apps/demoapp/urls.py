# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*{$english_name$}list\.html', views.{$english_name$}list, name='{$english_name$}list'),
    url(r'^.*create$', views.create),
    url(r'^.*delete$', views.delete),
    url(r'^.*reportdata', views.reportdata),
    url(r'^.*{$english_name$}data', views.{$english_name$}data),
    url(r'^.*{$english_name$}form\.html', views.{$english_name$}form),
    url(r'^.*template$', views.template_download),
    # The home page
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'^$', views.index, name='index'),
]
