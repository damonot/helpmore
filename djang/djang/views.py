from asyncio.windows_events import NULL
from django.http import HttpResponse
from django.shortcuts import render
from requests import get
from . import donation_amount_calc



def index(request):

    lastdono = 50

    lastdono = int( request.COOKIES.get('donation2', '0') )
    print(lastdono)

    ip = get('https://api.ipify.org').text
    rec_dono = donation_amount_calc.main(ip, lastdono)
    context = {"recdono": rec_dono}

    response = render(request, 'djang/index.html', context)

    response.set_cookie('donation', '100')

    return response
    