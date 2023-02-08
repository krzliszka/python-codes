from django.urls import path, include
from django.conf.urls.static import url
from .views import *
url_patterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
]
