import pandas as pd
import json
import requests
import os

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
    zip_table = pd.read_csv(cwd + '/djang/static/djang/US_Zip.csv',low_memory=False)
    us_median_income_table = zip_table.loc[:, ['NAME', 'S1901_C01_012E']]
    us_median_income_table['NAME'] = us_median_income_table['NAME'].map(lambda x: x.lstrip('ZCTA5').rstrip('aAbBcC'))
    series = us_median_income_table['S1901_C01_012E'].where(us_median_income_table['NAME'] == ((' ')+ zip))
    series = series.dropna()
    result = int(series.iloc[0])
    return (result)


def income_to_donation(income,last_donation):
    donation_amounts = [25,50,100, 250, 500]
    median_income = int(income)
    
    if median_income < 45000:
        return (donation_amounts)

    elif 45000 <= median_income < 100000:
        if last_donation > 0:
            donation_amounts = [last_donation, last_donation*2,last_donation *3,last_donation *4,last_donation *5]
            return (donation_amounts)
        else: 
            donation_amounts  = [element * 2 for element in donation_amounts]
            return (donation_amounts)  

    elif 100000 <= median_income < 200000:
        if last_donation > 0:
            donation_amounts = [last_donation, last_donation*2,last_donation *3,last_donation *4,last_donation *5]
            return (donation_amounts)
        else: 
            donation_amounts  = [element * 3 for element in donation_amounts]
            return (donation_amounts)

    elif median_income >= 200000:
        if last_donation > 0:
            donation_amounts = [last_donation, last_donation*2,last_donation *3,last_donation *4,last_donation *5]
            return (donation_amounts)
        else: 
            donation_amounts  = [element * 4 for element in donation_amounts]
            return (donation_amounts)
        

def main(ip):
    apiresponse = ipxapi(ip)
    income = zip_to_income(apiresponse.text)
    donos = income_to_donation(income, 50)
    print(type(donos))
    return donos