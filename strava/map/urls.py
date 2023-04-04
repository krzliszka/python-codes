from django.urls import path, include
from django.conf.urls.static import url
from .views import *

url_patterns = [
    path('', base_map, name='Base Map View'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
