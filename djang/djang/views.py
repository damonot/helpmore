from django.http import HttpResponse
from django.shortcuts import render
from requests import get
from . import donation_amount_calc

def index(request):
    ip = get('https://api.ipify.org').text
    lastdono = 50
    rec_dono = donation_amount_calc.main(ip, lastdono)
    context = {"recdono": rec_dono}
    response = render(request, 'djang/index.html', context)
    response.set_cookie('donation', '50')
    return response
    