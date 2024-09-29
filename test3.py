# import uuid

# # Generate a UUID4
# uuid_code = uuid.uuid4()

# # Convert the UUID to a string if needed
# uuid_str = str(uuid_code)

# print("UUID4 Code:", uuid_str)

import requests

url = 'http://0.0.0.0:8000/wallet_app/withdrawal-req/'
headers = {'Authorization': 'Token 983e948871952596642117adfeaf9340584e3e4a'}
data={
    "type":"MobileBank",
    "number":"0172765263",
    "bankName":"BKASH",
    "amount":100,
}
response = requests.post(url, headers=headers,data=data)

print(response.status_code)
try:
    print(response.json())
except:
    pass