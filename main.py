import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import copyright
from accounts import get_accounts
from biscuits import load_cookies, dump_cookies
from fbrequests import login, get_token, get_acc_info
from headers import set_useragent, set_headers
from proxies import get_proxies, set_proxy, update_proxy_link
from tndr import get_tinder_access_token

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
            if acc.cookies is not None:
                print("Account has cookies, adding them to request and skipping Log In...")
                load_cookies(session, acc.cookies)
            else:
                loggedin = login(session, acc.login, acc.password)
                # if not loggedin:
                #     update_proxy_link(pr[i])
                #     set_proxy(session, pr, i)
                #     loggedin = login(session, acc.login, acc.password)

                acc.cookies = json.dumps(dump_cookies(session.cookies))
                if not loggedin:
                    continue

            token = get_token(session)
            if token is None:
                print("Access Token not found!")
                continue
            print("Found Accesss Token!")
            acc.token = token
            if use_tinder:
                ttoken = get_tinder_access_token(session)
                if ttoken != None:
                    print("Got Tinder app token...")
                    info = get_acc_info(session, ttoken)
                    print("Got account info!")
                    acc.add_info(info)
            f.write(str(acc))
            f.flush()

    print("All done. Accounts with tokens and cookies written to parsed.txt file.")
