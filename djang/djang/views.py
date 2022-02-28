from django.http import HttpResponse
from django.shortcuts import render
from requests import get
from . import donation_amount_calc

def index(request):

    ip = get('https://api.ipify.org').text
    recommented_dono = donation_amount_calc.main(ip)
    #print(medianinc)
    context = {}
    return render(request, 'djang/index.html', context)
    