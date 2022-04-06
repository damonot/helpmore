from re import sub
from django.shortcuts import render
from requests import get
from . import donation_amount_calc, cookies, fiftyone_api

from .forms import DonationForm, Form2, DynamicForm


def writedono(list):
    MyFile=open('dono.txt','w')

    for element in list:
        MyFile.write(str(element))
        MyFile.write('\n')
    MyFile.close()

def index(request):

    cookies.main(request)

    userinfo = fiftyone_api.main(request)

    print(userinfo)

    lastdono = cookies.getcookie(request)
    ip = get('https://api.ipify.org').text
    recdono = donation_amount_calc.main(ip, lastdono)
    print(recdono)


    CHOICES= [
    ('0', str(recdono[0])),
    ('1', str(recdono[1])),
    ('2', str(recdono[2])),
    ('3', str(recdono[3])),
    ('4', str(recdono[4])),
    ]
    #form = Form2(request.POST, fields=CHOICES)
    form = DonationForm(request.POST)

    context = {"recdono": recdono, "form": form}
    response = render(request, 'djang/index.html', context)

    formdata = None
    if form.is_valid():
        formdata = form.cleaned_data.get("dono_options")

    if formdata is None:
        submitteddono = lastdono
    else:
        submitteddono = recdono[formdata-1]
    print("SUMBITTED DONO " + str(submitteddono))
    cookies.setcookie(response, submitteddono)

    tip = int(submitteddono * .15)
    link = "https://link.justgiving.com/v1/charity/donate/charityId/13441?donationValue="+str(submitteddono)+"&totalAmount="+str(submitteddono+tip)+"&currency=GBP&skipGiftAid=true&skipMessage=true"

    print(link)

    return response