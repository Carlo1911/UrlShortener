from django.contrib import admin
from django.urls import path
from Shortener import views
from django.conf import settings

urlpatterns = [
    path('shorten/', views.get_form, name='urlform')
]
