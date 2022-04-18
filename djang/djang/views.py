from array import array
from asyncio.windows_events import NULL
from http import client
from re import T, sub
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

    if 'previousDonation' in request.session:
        request.session['previousDonation']
    else:
        request.session['previousDonation'] = 0

    request.session.modified = True

    print('session '+str(request.session['previousDonation']))

    previousDonation = request.session['previousDonation']

    recommendedDonationsArray = donation_amount_calc.main(str(client_ip), previousDonation, userinfo)
    recomendedDonations = arrayToTupleList(recommendedDonationsArray)
    recommendedTips = formatTip(recommendedDonationsArray[2])

    radioDonations = RadioForm(request.POST, my_choices=recomendedDonations)
    tipDropdowns = DropdownForm(request.POST, my_choices=recommendedTips)
    inputDonation = InputForm(request.POST)

    context = {"radio": radioDonations, "dropdown": tipDropdowns, "input": inputDonation}
    
    response = render(request, 'djang/index.html', context)


    print("\n^CLIENT IP: "+str(client_ip)+\
        "\nrecommendedDonations: "+(str(recommendedDonationsArray)))

    radio_select = 0
    input_select = '' 
    print(radioDonations.is_valid())
    print(inputDonation.is_valid())
    if(radioDonations.is_valid()):
        radio_select= int(radioDonations.cleaned_data.get("my_field"))
        
        tip_select = int(tipDropdowns.cleaned_data.get("my_tip")[1:-3])
        input_select = inputDonation['my_input'].value()
        print("radio:" + str(radio_select))
        print("tip:" + str(tip_select))
        print("input:" + str(input_select))

        larger = computeLarger(radio_select, input_select)

        total = int(larger) + int(tip_select)

        link = "https://link.justgiving.com/v1/charity/donate/charityId/13441?donationValue="+str(larger)+"&totalAmount="+str(total)+"&currency=GBP&skipGiftAid=true&skipMessage=true"
        return redirect(link)
    else:
        print("input type...")
        print(type(input_select))
        input_select = inputDonation['my_input'].value()
        if(type(input_select) == str):
            if(input_select.isnumeric()):
                tip_select = int(tipDropdowns.cleaned_data.get("my_tip")[1:-3])
                print("input:" + str(input_select))       
                print("tip:" + str(tip_select))

                total = int(input_select) + int(tip_select)

                link = "https://link.justgiving.com/v1/charity/donate/charityId/13441?donationValue="+str(input_select)+"&totalAmount="+str(total)+"&currency=GBP&skipGiftAid=true&skipMessage=true"
                return redirect(link)
        else:  
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

def computeLarger(radio_select, input_select):

    if(type(input_select) == str):
        if(input_select.isnumeric()):
            if(int(input_select) > int(radio_select)):
                return input_select
            else:
                return radio_select
    else:
        return radio_select
