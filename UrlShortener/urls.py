from django.contrib import admin
from django.urls import path
from Shortener import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]
