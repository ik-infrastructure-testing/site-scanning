from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
import os

urlpatterns = [
	path('search200/', views.search200, name='search200'),
	path('search200/json/', views.search200json, name='search200json'),
	path('search200/csv/', views.search200csv, name='search200csv'),
	path('searchUSWDS/', views.searchUSWDS, name='searchUSWDS'),
    path('', views.index, name='index'),
]
