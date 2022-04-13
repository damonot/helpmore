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

    #print(userinfo)

    lastdono = cookies.getcookie(request)
    ip = get('https://api.ipify.org').text

    recdono = donation_amount_calc.main(ip, lastdono, userinfo)
    print(recdono)

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

    form_select = None
    if form.is_valid():
        form_select= int(form.cleaned_data.get("my_field"))

        if form_select is None:
            submitteddono = lastdono
        else:
            submitteddono = form_select
        print("SELECTED: "+str(form_select)+ "\tSUBMITTED: "+str(submitteddono))

        print("SETTING COOKIE TO: "+str(submitteddono))
        #response.set_cookie("donation", submitteddono)
        cookies.setcookie(response, submitteddono)
        print(cookies.getcookie(request))

        tip = int(submitteddono * .15)
        link = "https://link.justgiving.com/v1/charity/donate/charityId/13441?donationValue="+str(submitteddono)+"&totalAmount="+str(submitteddono+tip)+"&currency=GBP&skipGiftAid=true&skipMessage=true"
        return redirect(link)
        #return response
    else:
        cookies.setcookie(response, lastdono)
        return response