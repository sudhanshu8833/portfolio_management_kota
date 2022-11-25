import requests
from AesEverywhere import aes256
from ast import literal_eval
from pprint import pprint
######################################################################################################################
# APP SESSION ID
# url="https://stagingtradingorestapi.swastika.co.in/auth/SSO/GetSSOAppSessionId/"

# body={
#  "AccessKey": "LAKSGPT@APK1734#",
#  "AccessSecret": "AFE2253F-5A4F-4590-BA13-F69B3D8B5E10"
# }

# response=requests.post(url,json=body)
# response=response.json()

# # print("kdsjfklsdfjkl")
# # print(response)
# session_id=response["Result"]["Data"]["AppSessionId"]

# web_url=f"https://stagingjustradekb.swastika.co.in/auth/login?AppSessionId={session_id}&State=SWASTIKA"
# print(web_url)

######################################################################################################################
#GENERATING ACCESS TOKEN FROM encrypted

tthead="U2FsdGVkX18KmzRwlbVHflehmq2psrFs07jZbDGz4KapkIBeeR3mlT5bBerzOBWjCl1ZxE/7os9pjHJS4LNV2yMZ1VFTKbi54wmaap8MkXJ7xPqUJCYFtiJR0oh0K1gmvAKpPC7kDo8KWczvLxD8Q8/gEIH5/WvpuN3DHMBKyS9uZgDk4LZhWa17zeBaPPvbU8xotx49B1q8sPJg5JgnJxnVJSgdFeJ+fVHxoFrR9/BXiYzjLUEuHH5Qusg0nEypavnJbQVfVZb0dDqBSv/496Gd1W0Fnz/tgMNrQh1VqI668AuMbCkahmkL3rML9ZsHy1+h2QnZGFUOAqa6ZJJaZwf/oob9WQ553FnXFIjlg6bKwrnA8gVpeZRV/dG87y+0w3AFdUx21aNYUtZhCr0MyRTxb0qSk9xHvFZ+AbyCaIoUyd4G/oK9kOAeUp9NkgqPyxuFEg+rHy4a1R5jaE3K07/JakE9gDDbjzgS7J8rOt15wGp4NWpO3lEbEb1DqOCLdVJScUwTOkPA7JfIBUddHaY3WOanqwidxMVCUcdRC1FrITTGEhz1gT6lvhW86b7cLZQPfaSjoD4Iva+2bRT/Y0QGV6YfWQNzsj/lSFl8ldGFTEuf5fzK5djqYljr2XQTvvwfIM2DM5QTgbz7gcrnP+n4g9eS3EmROMMz+0VSIlaOpXNlzwzwgUlwnqYjAsuWy3Ihkh64ref1DyIurFYN35Im7Gl0rvaSONV75+J/i9bNRkAv7JVwrbIJ4SnMkV8IFNCh0ma1cryabCZlB/Wf2ATPjdFEUqMUD8JnYfvD4NPWjJanAu84uVCIe6Lsw7RQ0Zfl3Eezvdi77rAu9eCge4Ss3KMjWn1RiCcyiQYLQ7EuKZ85QwaOsHAbxpJC93oilZb09O+NXtwXh/cw8XWrRZ7qT51z67xT6Xs02eCjgo4lGRKOzuPKxlWUNURrrzopYwbfkWXv2rrVOdphIy/hmmURlI2fHNI71l3GmPGDtYY="
response_data=aes256.decrypt(tthead, '9E5000F4-6489-4D84-8B67-B8D8D481F9BB')
response_data=literal_eval(response_data.decode('utf-8'))
print(response_data["ClientCode"])

# print(response_data['AccessToken'])
access_token=str(response_data['AccessToken'])

######################################################################################################################
#GETTING SECURITY INFO

# url="https://stagingtradingorestapi.swastika.co.in/kb/PlaceOrders/GetSecurityInfo"


# headers={
#     "Authorization":f"Bearer {access_token}"
# }

# body={
# "Uid": "DEMO2",
# "Exch": "NFO",
# "Token": "42880"
# }



# decrypt=requests.post(url,headers=headers,json=body)
# print(decrypt)
# print(decrypt.content)

######################################################################################################################
# PLACE ORDER

# url="https://stagingtradingorestapi.swastika.co.in/kb/PlaceOrders/PlaceOrder"

# headers={
#     "Authorization":f"Bearer {access_token}"
# }

# # response_data=aes256.decrypt(decrypt.json()['Data'], '9E5000F4-6489-4D84-8B67-B8D8D481F9BB')
# # print(response_data)

# body={
#     "Uid": "DEMO2",
#     "Actid": "DEMO2",
#     "Exch": "NFO",
#     "Tsym": "NIFTY08DEC22P18500",
#     "Qty": "50",
#     "Prc": "0",
#     "Prd": "M",
#     "Trantype": "B",
#     "Prctyp": "MKT",
#     "Ret": "DAY"
#     }

# decrypt=requests.post(url,headers=headers,json=body)
# print(decrypt)
# print(decrypt.content)