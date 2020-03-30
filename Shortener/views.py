from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from Shortener.forms import URLDataForm
from Shortener.models import URLData
import string
import random


def base_encode(integer, alphabet=settings.BASE_LIST):  # Convert ID to FullURL
    """ Convert ID to FullURL """
    if integer == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while integer:
        integer, rem = divmod(integer, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base_decode(request, reverse_base=settings.BASE_DICT):
    """ Convert FullURL to ID """
    longurl = request
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(longurl[::-1]):
        ret += (length ** i) * reverse_base[c]
    return ret


def shortChars():  # Get Shortened URL endpoint
    SHORT_LIST_CHAR = '0123456789'+string.ascii_letters
    return ''.join([random.choice(SHORT_LIST_CHAR) for i in range(10)])


def checkIDExists(ID):
    """ Check to see if ID exists in DB """
    short_chars = str(shortChars())
    retreived_IDs = list(URLData.objects.values_list('URLID', flat=True))
    if str(ID) in retreived_IDs:
        short_url = URL_ID = URLData.objects.filter(URLID=str(ID)).first().ShortURL
        message = 'Record Already Exists. Link is: {}/{}'.format(settings.BASE_URL, short_url)
    else:
        url_data = URLData(URLID=ID, ShortURL=short_chars)
        url_data.save()
        message = ('Congratulatons! Your shortened URL is {}/{}'.format(settings.BASE_URL, short_chars))
    return message


def redirect_short_url(request, short_url):
    redirect_url = settings.BASE_URL
    try:
        URL_ID = URLData.objects.filter(ShortURL=short_url)[0].URLID
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
            messages.success(request, format(checkIDExists(ID)))
    form = URLDataForm()
    return render(request, 'form.html', {'form': form})
