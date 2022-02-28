from django.http import HttpResponse
from django.shortcuts import render
from requests import get
from . import donation_amount_calc

def index(request):

    ip = get('https://api.ipify.org').text
    rec_dono = donation_amount_calc.main(ip)
    context = {"recdono": rec_dono}
    return render(request, 'djang/index.html', context)
    