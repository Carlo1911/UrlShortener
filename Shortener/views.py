from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from django.core import serializers
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect
from Shortener.forms import URLDataForm
from Shortener.models import URLData
from Shortener.serializers import URLDataSerializers
import sqlite3
import string
import random


class FullURLView(viewsets.ModelViewSet):
    queryset = URLData.objects.all()
    serializers_class = URLDataSerializers


def base_encode(integer, alphabet=settings.BASE_LIST):  # Convert ID to FullURL
    if integer == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while integer:
        integer, rem = divmod(integer, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base_decode(request, reverse_base=settings.BASE_DICT):  # Convert Full URL to ID
    longurl = request
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(longurl[::-1]):
        ret += (length ** i) * reverse_base[c]
    return ret


def shortChars():  # Get Shortened URL endpoint
    SHORT_LIST_CHAR = '0123456789'+string.ascii_letters
    return ''.join([random.choice(SHORT_LIST_CHAR) for i in range(10)])


def checkIDExists(ID):  # Check to see if ID exists in DB
    sc = str(shortChars())
    Retreived_IDs = list(URLData.objects.values_list('URLID', flat=True))
    if str(ID) in Retreived_IDs:
        surl = URL_ID = URLData.objects.all().filter(URLID=str(ID))[0].ShortURL
        mess = "Record Already Exists. \n\nLink is: {}/{}".format(settings.BASE_URL, surl)
    else:
        U = URLData(URLID=ID, ShortURL=sc)
        U.save()
        mess = ("Congratulatons! Your shortened URL is {}/{}".format(settings.BASE_URL, sc))
    return mess


def redirect_short_url(request, short_url):
    redirect_url = settings.BASE_URL + '/shorten'
    URL_ID = URLData.objects.filter(ShortURL=short_url)[0].URLID
    redirect_url = base_encode(int(URL_ID))
    try:
        URL_ID = URLData.objects.filter(ShortURL=short_url)[0].URLID
        redirect_url = base_encode(int(URL_ID))
    except Exception as e:
        print(e)
        print('xD')
    return redirect(redirect_url)


def get_form(request):
    if request.method == 'POST':
        form = URLDataForm(request.POST)
        if form.is_valid():
            print('is valid')
            fullurl = form.cleaned_data['EnterURL']
            ID = base_decode(fullurl.lower())
            print('is valid x2')
            messages.success(request, ''.format(checkIDExists(ID)))
            print('is valid x3')
    form = URLDataForm()
    print('is valid x4')
    return render(request, 'form.html', {'form': form})
