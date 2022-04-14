from http import client
from re import sub
from django.shortcuts import render, redirect
from requests import get
from . import donation_amount_calc, cookies, fiftyone_api

from .forms import MyCustomForm


def writedono(list):
    MyFile=open('dono.txt','w')

    for element in list:
        MyFile.write(str(element))
        MyFile.write('\n')
    MyFile.close()

def index(request):

    cookies.main(request)

    userinfo = fiftyone_api.main(request)

    try:
        if client_ip != '127.0.0.1':
            client_ip = request.META['REMOTE_ADDR']
        else:
            client_ip == '8.8.8.8'
    except:
        client_ip = '8.8.8.8'


    lastdono = cookies.getcookie(request)

    recdono = donation_amount_calc.main(str(client_ip), lastdono, userinfo)


    list_of_tuples=[    
    (str(recdono[0]), str(recdono[0])),
    (str(recdono[1]), str(recdono[1])),
    (str(recdono[2]), str(recdono[2])),
    (str(recdono[3]), str(recdono[3])),
    (str(recdono[4]), str(recdono[4])),
    ]
    form = MyCustomForm(request.POST, my_choices=list_of_tuples)

    context = {"recdono": recdono, "form": form}
    
    response = render(request, 'djang/index.html', context)


    print("\n^CLIENT IP: "+str(client_ip)+\
        "\nRECDONO: "+(str(recdono)))

    form_select = None
    if form.is_valid():
        form_select= int(form.cleaned_data.get("my_field"))

        if form_select is None:
            submitteddono = lastdono
        else:
            submitteddono = form_select
        # print("SELECTED: "+str(form_select)+ "\tSUBMITTED: "+str(submitteddono))

        # print("SETTING COOKIE TO: "+str(submitteddono))
        #response.set_cookie("donation", submitteddono)
        cookies.setcookie(response, submitteddono)
        # print(cookies.getcookie(request))

        tip = int(submitteddono * .15)
        link = "https://link.justgiving.com/v1/charity/donate/charityId/13441?donationValue="+str(submitteddono)+"&totalAmount="+str(submitteddono+tip)+"&currency=GBP&skipGiftAid=true&skipMessage=true"
        return redirect(link)
        #return response
    else:
        cookies.setcookie(response, lastdono)
        return response