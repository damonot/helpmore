import pandas as pd
import json
import requests
import os
from sklearn.linear_model import LinearRegression
import numpy as np

def ipxapi(ip):
    url = "https://ipxapi.com/api/ip?ip="+ip
    
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer 825|TYdYvsByrjJPNR7qk7srT1I1BJk5EEsPskHS4tk4",
        'cache-control': "no-cache"
    }
    
    response = requests.request("GET", url, headers=headers)
    return response


def zip_to_income(data):
    ip_info = data
    ip_info = json.loads(data)
    zip = ip_info['zip']
    
    cwd = os.getcwd()
    f = open(cwd + '/djang/static/djang/Zip_Table.json')
    zip_table = json.load(f)
    income = int(zip_table[zip]['INCOME'])
    f.close()
    return income
    

def round_to_five(number):
    return 5 * round(number / 5)

def regression_to_donation(pred_donation):
    suggested_donations = []
    predicted_donation = int(pred_donation)
    suggested = np.linspace(25,predicted_donation,5)
    
    for dono in suggested:
        suggested_donations.append(round_to_five(dono))
    return suggested_donations

def regression(median_income,last_donation, fiftyone_data):
    data = {'MedianIncome': [15000,20000,40000,75000,150000,200000,14000,27000,34000,50000,100000,250000], 
            'PrevDonation':[0,0,0,0,0,0,45,90,66,105,50,125],
            'CurrDonation':[100, 133.33, 233.33, 312.5, 375, 500, 83, 180,198.33,208.33,250,625],
            'HardwareVendor':['Android','Apple','Android','Apple','Android','Apple','Apple','Apple','Android','Android',
                           'Android','Apple'],
            'BrowserName': ['Other', 'IE', 'Chrome', 'Chrome', 'Safari', 'Safari', 'Other', 'IE','Firefox','Firefox','Chrome',
                       'Safari']
            
            
           }

    df = pd.DataFrame(data)
    #Encode Categorical Data
    df = pd.get_dummies(df, columns=["HardwareVendor", 'BrowserName'])
    #CleanUp Inputs
    last_donation = float(last_donation)
    hardware_vendor = fiftyone_data['hardwarevendor']
    browser_name = fiftyone_data['browsername']
    #device_type = fiftyone_data['devicetype']
    
    
    if hardware_vendor == 'Apple':
            hardware_vendor_apple = 1
            hardware_vendor_android = 0
    else:
            hardware_vendor_android = 1
            hardware_vendor_apple = 0
            
            
    bnames = np.zeros(5,dtype=int)
    if "Chrome" in browser_name:
        bnames[0] = 1
    if "Safari" in browser_name:
        bnames[1] = 1
    if "Firefox" in browser_name:
        bnames[2] = 1
    if ("Internet Explorer") in browser_name:
        bnames[3] = 1
    elif browser_name not in data['BrowserName']:
        browser_name = 'Other'
        bnames[-1] = 1
    
    x = df[['MedianIncome','PrevDonation','HardwareVendor_Android','HardwareVendor_Apple', 
            'BrowserName_Chrome','BrowserName_Safari', 'BrowserName_Firefox', 'BrowserName_IE', 'BrowserName_Other']]
    y = df['CurrDonation'].values.reshape(-1,1)
    model = LinearRegression().fit(x, y)

    #Predict Donation Amount
    y_pred = model.predict([[median_income,
                             last_donation, hardware_vendor_android, hardware_vendor_apple, 
                             bnames[0],bnames[1],bnames[2],bnames[3],bnames[4]]])
    pred_donation = round_to_five(y_pred[0][0])
    
    if last_donation != 0: 
        sugg_donation = [last_donation,last_donation * 2, last_donation *3, last_donation * 4,last_donation*5]
        return sugg_donation
    else:
        return (regression_to_donation(pred_donation))
    
    #append df with median_income,last_donation, and curr donation when we have real data#

def main(ip, lastdono, userinfo):
    apiresponse = ipxapi(ip)
    income = zip_to_income(apiresponse.text)
    donos = regression(income, lastdono, userinfo)
    return donos