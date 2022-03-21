from django.shortcuts import render
from requests import get
from . import donation_amount_calc, cookies, user_agent_api, fiftyone_api



def index(request):

    cookies.main(request)

    user_agent_parse = user_agent_api.main(request)
    fiftyone_api.main(request)

    lastdono = cookies.getcookie(request)
    ip = get('https://api.ipify.org').text
    recdono = donation_amount_calc.main(ip, lastdono)
    context = {"recdono": recdono}

    response = render(request, 'djang/index.html', context)
    #TODO get submitteddono from page
    submitteddono = 100
    cookies.setcookie(response, submitteddono)

    return response