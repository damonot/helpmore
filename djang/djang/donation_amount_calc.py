import pandas as pd
import json
import requests
import os
from sklearn.linear_model import LinearRegression

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

def round_to_five(number):
    return 5 * round(number / 5)

def regression_to_donation(pred_donation):
    suggested_donations = []
    predicted_donation = int(pred_donation)
    suggested = np.linspace(25,predicted_donation,5)
    
    for dono in suggested:
        suggested_donations.append(round_to_five(dono))
    return suggested_donations

def regression(median_income,last_donation):
    data = {'MedianIncome': [15000,20000,40000,75000,150000,200000,14000,27000,34000,50000,100000,250000], 
            'PrevDonation':[0,0,0,0,0,0,45,90,66,105,50,125],
            'CurrDonation':[100, 133.33, 233.33, 312.5, 375, 500, 83, 180,198.33,208.33,250,625]}
    df = pd.DataFrame(data)
    
    x = df[['MedianIncome','PrevDonation']]
    y = df['CurrDonation'].values.reshape(-1,1)
    model = LinearRegression().fit(x, y)
    
     if last_donation != 0: 
        sugg_donation = [last_donation,last_donation * 2, last_donation *3, last_donation * 4,last_donation*5]
        return sugg_donation
    else:
        last_donation = float(last_donation)
        y_pred = model.predict([[income,last_donation]])
        pred_donation = round_to_five(y_pred[0][0])
        return (regression_to_donation(pred_donation))
    
    #append df with median_income,last_donation, and curr donation when we have real data#

def main(ip, lastdono):
    apiresponse = ipxapi(ip)
    income = zip_to_income(apiresponse.text)
    donos = regression(income, lastdono)
    return donos