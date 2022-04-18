from array import array
from http import client
from re import sub
from django.shortcuts import render, redirect
from requests import get
from . import donation_amount_calc, cookies, fiftyone_api
from .forms import DropdownForm, RadioForm, InputForm


def index(request):

    cookies.main(request)

    userinfo = fiftyone_api.main(request) # Get MetaData

    try:
        if client_ip != '127.0.0.1':
            client_ip = request.META['REMOTE_ADDR']
        else:
            client_ip == '8.8.8.8'
    except:
        client_ip = '8.8.8.8'


    previousDonation = cookies.getcookie(request)

    recommendedDonationsArray = donation_amount_calc.main(str(client_ip), previousDonation, userinfo)
    recomendedDonations = arrayToTupleList(recommendedDonationsArray)
    recommendedTips = formatTip(recommendedDonationsArray[2])

    radioDonations = RadioForm(request.POST, my_choices=recomendedDonations)
    tipDropdowns = DropdownForm(request.POST, my_choices=recommendedTips)
    inputForm = InputForm()

    context = {"radio": radioDonations, "dropdown": tipDropdowns, "input": inputForm}
    
    response = render(request, 'djang/index.html', context)


    print("\n^CLIENT IP: "+str(client_ip)+\
        "\nrecommendedDonations: "+(str(recommendedDonationsArray)))

    radio_select = None
    if radioDonations.is_valid():
        radio_select= int(radioDonations.cleaned_data.get("my_field"))
        print("radio:" + str(radio_select))

        tip_select = int(tipDropdowns.cleaned_data.get("my_tip"))
        print("tip:" + str(tip_select))

        input_select = inputForm['my_input'].value()
        print("input:" + str(input_select))


    

    #     if radio_select is None:
    #         submitteddono = previousDonation
    #     else:
    #         submitteddono = radio_select

    # tip_select = 0
    # if tipDropdowns.is_valid():
    #     tip_select = int(tipDropdowns.cleaned_data.get("my_field"))
    #     print("tip:" + str(tip_select))
    #     # print("SELECTED: "+str(radio_select)+ "\tSUBMITTED: "+str(submitteddono))

    #     # print("SETTING COOKIE TO: "+str(submitteddono))
    #     #response.set_cookie("donation", submitteddono)
    #     # cookies.setcookie(response, submitteddono)
    #     # print(cookies.getcookie(request))

    #     tip = int(submitteddono * .15)
    #     link = "https://link.justgiving.com/v1/charity/donate/charityId/13441?donationValue="+str(submitteddono)+"&totalAmount="+str(submitteddono+tip)+"&currency=GBP&skipGiftAid=true&skipMessage=true"
    #     return redirect(link)
    #     #return response
    # else:
    #     cookies.setcookie(response, previousDonation)
    return response

def arrayToTupleList(arr):
    tups = []
    for x in arr:
        t = (str(x), (x))
        tups.append(t)
    return tups

def formatTip(arr):
    tips = [0]
    for x in range (2,7) :
        if (arr/x) not in tips:
            tips.append(int(arr/x))
    tips.sort()
    tips = [5*round(x/5) for x in tips]
    s = [("$"+str(x)+".00") for x in tips]
    tups = arrayToTupleList(s)
    return tups
