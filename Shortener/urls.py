from django.urls import path
from Shortener import views

urlpatterns = [
    path('', views.get_form, name='urlform'),
    path('<str:short_url>/', views.redirect_short_url, name='redirect_function'),
]
