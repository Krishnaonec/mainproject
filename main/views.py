from django.shortcuts import render
from decouple import config
# Create your views here.

def index(request):
    return render(request, 'main/index.html', {'WEBEX_AUTH_LINK': config('WEBEX_AUTH_LINK')})