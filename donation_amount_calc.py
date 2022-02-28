import pandas as pd
import json
import requests
def zip_to_income(data):
    ip_info = pd.json_normalize(data)
    ip_info = ip_info['zip'].astype('str')
    ip_to_zip = ip_info.iloc[0]
    
    zip_table = pd.read_csv('US_Zip.csv',low_memory=False)
    us_median_income_table = zip_table.loc[:, ['NAME', 'S1901_C01_012E']]
    us_median_income_table['NAME'] = us_median_income_table['NAME'].map(lambda x: x.lstrip('ZCTA5').rstrip('aAbBcC'))
    series = us_median_income_table['S1901_C01_012E'].where(us_median_income_table['NAME'] == ((' ')+ ip_to_zip))
    series = series.dropna()
    result = int(series.iloc[0])
    return json.dumps(result)

#testing
ip_address = '2601:741:8002:ded0:cb1:b9e5:9091:9144'

url = "https://ipxapi.com/api/ip?ip="+ip_address
                
headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer 765|lezHXaW8lTxWHPTgCjAeKHgv5rAZqlKhVax0AIut",
        'cache-control': "no-cache"
                    }
response = requests.request("GET", url, headers=headers)
data = response.json()
median_income = zip_to_income(data)
print(median_income)

import json
def income_to_donation(income,last_donation):
    donation_amounts = [25,50,100, 250, 500]
    median_income = int(income)
    
    if median_income < 45000:
        return json.dumps(donation_amounts)
    
    
    
    elif 45000 <= median_income < 100000:
        if last_donation > 0:
            donation_amounts = [last_donation, last_donation*2,last_donation *3,last_donation *4,last_donation *5]
            return json.dumps(donation_amounts)
        else: 
            donation_amounts  = [element * 2 for element in donation_amounts]
            return json.dumps(donation_amounts)
        
        
        
    
    elif 100000 <= median_income < 200000:
        if last_donation > 0:
            donation_amounts = [last_donation, last_donation*2,last_donation *3,last_donation *4,last_donation *5]
            return json.dumps(donation_amounts)
        else: 
            donation_amounts  = [element * 3 for element in donation_amounts]
            return json.dumps(donation_amounts)
        
        
        
    
    elif median_income >= 200000:
        if last_donation > 0:
            donation_amounts = [last_donation, last_donation*2,last_donation *3,last_donation *4,last_donation *5]
            return json.dumps(donation_amounts)
        else: 
            donation_amounts  = [element * 4 for element in donation_amounts]
            return json.dumps(donation_amounts)
        
        
    
        
#Testing

print(income_to_donation(median_income,0))


