from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests,json
from copyright import Copyright
from headers import Headers
from biscuits import Biscuits
from parsing import Parsing
from proxies import Proxies
#from tinder import Tinder
from fbrequests import FB

def get_accounts():
    accounts = []
    afile = open("accounts.txt", "r")
    alines = afile.readlines()
    for a in alines:
        acs = a.strip().split(":")
        acc={"login": acs[0], "password": acs[1]}
        cookies= Parsing.get_cookies(a)
        if cookies!=None:
            acc["cookies"]=cookies
        accounts.append(acc)
    return accounts

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    Copyright.copyright()
    tanswer=input("Do you want to get birthday and email, using Tinder app?(Y/N)")
    tndr = Tinder() if (tanswer == "Y" or tanswer=="y") else None
    
    pr = Proxies.get_proxies()
    accounts = get_accounts()
    with open("parsed.txt", "w") as f:
        for i,acc in enumerate(accounts):
            uname = acc["login"]
            password = acc["password"]
            print(f"\nProcessing account {uname}:{password}...")

            session = requests.session()
            Headers.set_headers(session)
            Headers.set_useragent(session)
            Proxies.set_proxy(session, pr, i)
            if "cookies" in acc:
                print("Account has cookies, adding them to request and skipping Log In...")
                loggedin=True
                Biscuits.load_cookies(session,acc['cookies'])
            else:
                loggedin = FB.login(session, uname, password)

            if not loggedin:
                continue
            token = FB.get_token(session)
            if token == None:
                print("Token not found!")
                continue
            print("Found Accesss Token!")
            acc["cookies"] = json.dumps(Biscuits.dump_cookies(session.cookies))
            acc["token"] = token
            if tndr != None:
                ttoken = tndr.get_fb_access_token(uname, password)
                if ttoken.startswith("EAA"):
                    print("Got Tinder app token...")
                    info = tndr.get_acc_info(ttoken)
                    print("Got account info!")
                    if "email" in info:
                        f.write(
                            f"{acc['login']}:{acc['password']}:{info['birthday']}:{info['email']}:{acc['token']}:{acc['cookies']}\n"
                        )
                    else:
                        f.write(
                            f"{acc['login']}:{acc['password']}:{info['birthday']}:{acc['token']}:{acc['cookies']}\n"
                        )
                else:
                    print("Couldn't get Tinder app token(")
                    f.write(
                        f"{acc['login']}:{acc['password']}:{acc['token']}:{acc['cookies']}\n"
                    )
            else:
                f.write(
                    f"{acc['login']}:{acc['password']}:{acc['token']}:{acc['cookies']}\n"
                )
            i += 1

    print("All done. Accounts with tokens and cookies written to parsed.txt file.")
