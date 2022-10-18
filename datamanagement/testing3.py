from nsepython import *
import requests
import json
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
}
print("running")
payload = expiry_list('NIFTY')
print(payload)

# with open('option_chain_scrape.json', 'w') as fp:
#     json.dump(payload, fp)
# payload='https://www.nseindia.com/api/holiday-master?type=trading'
# output = requests.get(payload,headers=headers).json()
# print(output['FO'])
# with open('datamanagement/option_chain_scrape.json') as json_file:
#     data = json.load(json_file)
#     print(data)