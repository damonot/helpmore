from django.shortcuts import render
from requests import get
from . import donation_amount_calc, cookies, fiftyone_api

from .forms import DonationForm


def writedono(list):
    MyFile=open('dono.txt','w')

    for element in list:
        MyFile.write(str(element))
        MyFile.write('\n')
    MyFile.close()

def index(request):

    cookies.main(request)

    userinfo = fiftyone_api.main(request)

    #print(userinfo)

    lastdono = cookies.getcookie(request)
    ip = get('https://api.ipify.org').text
    recdono = donation_amount_calc.main(ip, lastdono, userinfo)

    writedono(recdono)

    context = {"recdono": recdono, "form": DonationForm()}

    response = render(request, 'djang/index.html', context)
    
    form= DonationForm(request.POST or None)
    
    formdata = None
    if form.is_valid():
        formdata= form.cleaned_data.get("dono_options")
        # print(data)
        # print(recdono[data])

    submitteddono = recdono[formdata]
    cookies.setcookie(response, submitteddono)
    return response
    
