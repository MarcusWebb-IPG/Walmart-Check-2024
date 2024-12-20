import requests as rq
import pwinput as pwi


def output_result(
    _json: dict,
    _email: str,
    _partner_name: str,
    _partner_id: str,
    _total_count: str,
):
    print("\n\nPartner Details")
    print("---------------")
    print(f"  Email Address : {_email}")
    print(f"   Partner Name : {_partner_name}")
    print(f"     Partner Id : {_partner_id}")

    try:
        advertiser_name = _json["AdvertiserName"]
        advertiser_id = _json["AdvertiserId"]
        currency_code = _json["CurrencyCode"]
        print(f"Advertiser Name : {advertiser_name}")
        print(f"  Advertiser Id : {advertiser_id}")
        print(f"  Currency Code : {currency_code}")
        print("===========================================")
        print(f" Total Running Campaign count: {_total_count}")

    except IndexError:
        print("\n[WARNING] - No campaigns appear to be active on this Advertiser ID")

    return


def api_checks(
    _email: str,
    _password: str,
    _partner_id: str,
):

    headers = {"Content-Type": "application/json"}
    data = {"Login": f"{_email}", "Password": f"{_password}"}

    base_url = "https://api.dsp.walmart.com/v3/"
    url = base_url + "authentication"

    res = rq.post(url=url, headers=headers, json=data)
    if res.status_code != 200:
        print(f"\nThe email address {_email} is causing a {res.status_code} error")
        return res.status_code, res.text, "No Partner Name yet", 0

    tok = res.json()["Token"]

    url = base_url + f"partner/{_partner_id}"
    headers = {"Content-Type": "application/json", "TTD-Auth": f"{tok}"}

    res = rq.get(url=url, headers=headers)
    if res.status_code != 200:
        print(f"\nThe email address {_email} is causing a {res.status_code} error")
        return res.status_code, res.json(), "Access to Partner not Authorized", 0
    # moved below the call in case no valid JSON is returned
    partner_name = res.json()["PartnerName"]

    url = base_url + "advertiser/query/partner"
    headers = {"Content-Type": "application/json", "TTD-Auth": f"{tok}"}
    data = {"PartnerId": f"{_partner_id}", "PageStartIndex": 0, "PageSize": 1}

    res = rq.post(url=url, headers=headers, json=data)
    if res.status_code != 200:
        print(f"\nProblem with {partner_name}: returning a {res.status_code} error")
        return res.status_code, res.text, partner_name, 0

    result = res.json()["Result"]
    total_count = res.json()["TotalUnfilteredCount"]

    return res.status_code, result[0], partner_name, total_count


def main():
    emails = ["wmt_api_matterkind@cadreon.com"]

    email = input("\nPlease provide email address to validate : ")

    emails.insert(0, email)
    start = email.find("i_") + 2
    end = email.find("@")
    partnerId = email[start:end]
    chk = input(f"Is the Partner ID {partnerId} valid? [Y/n] ")
    if chk == "y" or chk == "Y" or chk == "":
        pass
    else:
        partnerId = input(f"Please provide ID for {email} : ")

    # Now we check to make sure that the provided email address
    # and api@cadreon.com have access

    for email in emails:

        print(f"\nChecking connectivity at Walmart for {email}")
        pword = pwi.pwinput(prompt=f"\nProvide the password for address {email}:\n\t")

        stat_code, result, partner_name, total_count = api_checks(
            email, pword, partnerId
        )

        if stat_code == 200:
            print("\nSuccessful - see below\n")
            output_result(result, email, partner_name, partnerId, total_count)
        else:
            print("\nUnsuccessful - see above for details")
            print(f"Result of call:\n==============\n{result}\n")


if __name__ == "__main__":
    main()
