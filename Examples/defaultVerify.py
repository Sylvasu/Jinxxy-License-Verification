import requests

JINXXY_TOKEN = 'Jinxxy API token goes here'
PRODUCT_ID_EXPECTED = 1234567890
short_license_key = 'Short key goes here'

data = requests.get(
    "https://api.creators.jinxxy.com/v1/licenses",
    headers={
    "x-api-key": f"{JINXXY_TOKEN}"
    },
    params={
    "short_key": f"{short_license_key}",
    }
    
)
print(data)
if data.status_code == 401:
    print("please contact an admin stating that there was an error ccode 401:1, Thanks!")
elif data.status_code == 403:
    print("please contact an admin stating that there was an error ccode 403:1, Thanks!")
elif data.status_code == 429:
    print("please contact an admin stating that there was an error ccode 429:1, Thanks!")
elif data.status_code == 200:
    #Successful location of license ID
    responseJsonDat = data.json()
    licenseID = responseJsonDat['results'][0]['id']
    lisenceCheck = requests.get(
        f"https://api.creators.jinxxy.com/v1/licenses/{licenseID}",
        headers={
        "x-api-key": f"{JINXXY_TOKEN}"
        }
    )
    licenseJSON = lisenceCheck.json()
    retreivedProdId = int(licenseJSON['inventory_item']['item']['id'])
    print(retreivedProdId)
    if lisenceCheck.status_code == 401:
        print("please contact an admin stating that there was an error ccode 401:1, Thanks!")
    elif lisenceCheck.status_code == 403:
        print("please contact an admin stating that there was an error ccode 403:1, Thanks!")
    elif lisenceCheck.status_code == 404:
        print("License key does not exist. Please make sure you are using the correct key")
    elif lisenceCheck.status_code == 429:
        print("please contact an admin stating that there was an error ccode 429, Thanks!")
    elif lisenceCheck.status_code == 200:
        if retreivedProdId == PRODUCT_ID_EXPECTED:
            #Successful Verification
            print("License key is valid")
        else:
            #unsuccessful
            print("License key is not valid")
