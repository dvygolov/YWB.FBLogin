from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests, json
from accounts import get_accounts
from proxies import get_proxies, set_proxy
from headers import set_useragent, set_headers 
from biscuits import load_cookies, dump_cookies
from tndr import get_tinder_access_token
from fbrequests import login, get_token, get_acc_info
import copyright 

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    copyright.show()
    tanswer = input("Do you want to get birthday and email, using Tinder app?(Y/N)")
    use_tinder = True if (tanswer == "Y" or tanswer == "y") else False

    pr = get_proxies()
    accs = get_accounts()
    with open("parsed.txt", "w") as f:
        for i, acc in enumerate(accs):
            print(f"\nProcessing account {acc.login}:{acc.password}...")

            session = requests.session()
            set_headers(session)
            set_useragent(session)
            set_proxy(session, pr, i)
            if acc.cookies!=None:
                print(
                    "Account has cookies, adding them to request and skipping Log In..."
                )
                loggedin = True
                load_cookies(session, acc.cookies)
            else:
                loggedin = login(session, acc.login, acc.password)

            if not loggedin:
                continue
            token = get_token(session)
            if token == None:
                print("Access Token not found!")
                continue
            print("Found Accesss Token!")
            acc.cookies = json.dumps(dump_cookies(session.cookies))
            acc.token = token
            if use_tinder:
                ttoken = get_tinder_access_token(session)
                if ttoken != None:
                    print("Got Tinder app token...")
                    info = get_acc_info(session,ttoken)
                    print("Got account info!")
                    acc.add_info(info)
            f.write(str(acc))
            i += 1
            f.flush()

    print("All done. Accounts with tokens and cookies written to parsed.txt file.")
