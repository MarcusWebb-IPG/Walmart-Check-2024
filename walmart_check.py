import requests as rq
import pwinput as pwi

print("WALMART ACCOUNT VALIDATION")
print("==========================")
print("This routine only works on email addresses that are ")
print("formatted as wmt_api_<<partner_id>>@<<domain>>")
print("or those formatted as wmt_api_<<partner_id>>_rmn@<<domain>>")
print("Other formatted email addresses will fail\n")
email = input("Please provide email address to validate :")
pword = pwi.pwinput(prompt=f"Provide the password for address {email}:\n")

start = email.find("i_") + 2
end = email.find("@")
rmn_check = email.find("_rmn")
if rmn_check != -1:
    end = rmn_check
partnerId = email[start:end]
headers = {"Content-Type": "application/json"}

data = {"Login": f"{email}", "Password": f"{pword}"}

base_url = "https://api.dsp.walmart.com/v3/"
url = base_url + "authentication"

res = rq.post(url=url, headers=headers, json=data)

if res.status_code != 200:
    print(f"The email address {email} is causing a {res.status_code} error")
    exit(res.status_code)

tok = res.json()["Token"]

url = base_url + f"partner/{partnerId}"
headers = {"Content-Type": "application/json", "TTD-Auth": f"{tok}"}

res = rq.get(url=url, headers=headers)

if res.status_code != 200:
    print(f"The email address {email} is causing a {res.status_code} error")
    exit(res.status_code)

partner_name = res.json()["PartnerName"]
url = base_url + "advertiser/query/partner"
headers = {"Content-Type": "application/json", "TTD-Auth": f"{tok}"}
data = {"PartnerId": f"{partnerId}", "PageStartIndex": 0, "PageSize": 1}

res = rq.post(url=url, headers=headers, json=data)
result = res.json()["Result"]

if res.status_code != 200:
    print(f"Problem with {partner_name}: returning a {res.status_code} error")
    exit(res.status_code)

advertiser_id = result[0]["AdvertiserId"]
advertiser_name = result[0]["AdvertiserName"]
currency_code = result[0]["CurrencyCode"]
total_count = res.json()["TotalUnfilteredCount"]

print("\n\nPartner Details")
print("---------------")
print(f"  Email Address : {email}")
print(f"   Partner Name : {partner_name}")
print(f"     Partner Id : {partnerId}")
print(f"Advertiser Name : {advertiser_name}")
print(f"  Advertiser Id : {advertiser_id}")
print(f"  Currency Code : {currency_code}")
print("===========================================")
print(f" Total Running Campaign count: {total_count}")
