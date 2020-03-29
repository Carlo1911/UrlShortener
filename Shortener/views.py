from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.core import serializers
from django.contrib import messages
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.db import connection
from django.shortcuts import redirect
from Shortener.forms import URLDataForm
from Shortener.models import URLData
import sqlite3
import string
import random


def base_decode(arg):
    pass

def base_encode(arg):
    pass

def checkIDExists(arg):
    pass

def redirect_short_url(request, short_url):
    redirect = settings.BASE_URL + '/shorten'
    try:
        URL_ID = URLData.objects.all().filter(ShortURL=short_url)[0].URLID
        redirect_url = base_encode(int(URL_ID))
    except Exception as e:
        print(e)
    return redirect(redirect_url)

def get_form(request):
    if request.method == 'POST':
        form = URLDataForm(request.POST)
        if form.is_valid():
            fullurl = form.cleaned_data['EnterURL']
            ID = base_decode(fullurl.lower())
            messages.success(request, ''.format(checkIDExists(ID)))
    form = URLDataForm()
    return render(request, 'myform/form.html', {'form': form})
