from array import array
from asyncio.windows_events import NULL
from http import client
from re import T, sub
from django.shortcuts import render, redirect
from requests import get
from . import donation_amount_calc, fiftyone_api
from .forms import DropdownForm, RadioForm, InputForm


def index(request):

    userinfo = fiftyone_api.main(request) # Get MetaData
    try:
        if client_ip != '127.0.0.1':
            client_ip = request.META['REMOTE_ADDR']
        else:
            client_ip == '172.21.208.1'
    except:
        client_ip = '172.21.208.1'

    print("Processing for IPV4: "+str(client_ip))
    # request.session['previousDonation'] = 0

    print("\tPrevious Donation: " + str(request.session['previousDonation'])+"\n")
    if 'previousDonation' in request.session:
        previousDonation = request.session['previousDonation']
    else:
        previousDonation = 0

    recommendedDonationsArray = donation_amount_calc.main(str(client_ip), previousDonation, userinfo)
    recomendedDonations = arrayToTupleList(recommendedDonationsArray)
    recommendedTips = formatTip(recommendedDonationsArray[2])

    print("\n\t"+str(userinfo))
    print("\n\t"+str(recommendedDonationsArray))

    radioDonations = RadioForm(request.POST, my_choices=recomendedDonations)
    tipDropdowns = DropdownForm(request.POST, my_choices=recommendedTips)
    inputDonation = InputForm(request.POST)

    context = {"radio": radioDonations, "dropdown": tipDropdowns, "input": inputDonation}
    
    response = render(request, 'djang/index.html', context)

    radio_select = 0
    input_select = '' 
    tip_select = 0
    # print("RADIO valid? "+ str(radioDonations.is_valid()))

    if(radioDonations.is_valid()):
        radio_select= int(radioDonations.cleaned_data.get("my_radio"))
        tip_select = int(tipDropdowns.cleaned_data.get("my_tip")[0:-3])
        input_select = inputDonation['my_input'].value()

        larger = computeLarger(radio_select, input_select)

        # print(str(radio_select) + " RADIO: " + str(radio_select))
        # print(str(larger) + " TIP: " + str(tip_select))
        total = int(larger) + int(tip_select)

        request.session['previousDonation'] = total
        request.session.modified = True

        link = "https://link.justgiving.com/v1/charity/donate/charityId/60816?donationValue="+str(larger)+"&totalAmount="+str(total)+"&currency=GBP&skipGiftAid=true&skipMessage=true"
        return redirect(link)
    else:
        input_select = inputDonation['my_input'].value()

        if(type(input_select) == str and
            len(input_select) != 0 and
            input_select.isnumeric()):
            # print("TIP:"+ str(type(tip_select)) + " " + str(tip_select))
            tip_select = int(tipDropdowns.cleaned_data.get("my_tip")[0:-3])

            total = int(input_select) + int(tip_select)
            request.session['previousDonation'] = total
            request.session.modified = True

            link = "https://link.justgiving.com/v1/charity/donate/charityId/60816?donationValue="+str(input_select)+"&totalAmount="+str(total)+"&currency=GBP&skipGiftAid=true&skipMessage=true"
            return redirect(link)
        else:  
            return response

def arrayToTupleList(arr):
    tups = []
    for x in arr:
        t = (str(x), "£"+str((x)))
        tups.append(t)
    return tups

def formatTip(arr):
    tips = [0]
    for x in range (2,7) :
        if (arr/x) not in tips:
            tips.append(int(arr/x))
    tips.sort()
    tips = [5*round(x/5) for x in tips]
    s = [(str(x)+".00") for x in tips]
    tups = arrayToTupleList(s)
    return tups

def computeLarger(radio_select, input_select):

    if(type(input_select) == str and
        len(input_select) != 0 and
        input_select.isnumeric()):
            if(int(input_select) > int(radio_select)):
                return input_select
            else:
                return radio_select
    else:
        return radio_select
