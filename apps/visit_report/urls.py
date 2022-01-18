from django.conf.urls import url
from . import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*visitdata', views.get_trand_data),

    # The home page
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'^.*$', views.index, name='index'),
]
