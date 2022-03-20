from django.shortcuts import render
from requests import get
from . import donation_amount_calc, cookies



def index(request):

    cookies.main(request)

    lastdono = cookies.getcookie(request)
    ip = get('https://api.ipify.org').text
    recdono = donation_amount_calc.main(ip, lastdono)
    context = {"recdono": recdono}

    response = render(request, 'djang/index.html', context)
    #TODO get submitteddono from page
    submitteddono = 510
    cookies.setcookie(response, submitteddono)

    return response
    