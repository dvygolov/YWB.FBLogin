from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests,json
import copyright, headers, biscuits, parsing, proxies, fbrequests, tndr

def get_accounts():
    accounts = []
    afile = open("accounts.txt", "r")
    alines = afile.readlines()
    for a in alines:
        acs = a.strip().split(":")
        acc={"login": acs[0], "password": acs[1]}
        cookies= parsing.get_cookies(a)
        if cookies!=None:
            acc["cookies"]=cookies
        accounts.append(acc)
    return accounts

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    copyright.show()
    tanswer=input("Do you want to get birthday and email, using Tinder app?(Y/N)")
    use_tinder = True if (tanswer == "Y" or tanswer=="y") else False
    
    pr = proxies.get_proxies()
    accounts = get_accounts()
    with open("parsed.txt", "w") as f:
        for i,acc in enumerate(accounts):
            uname = acc["login"]
            password = acc["password"]
            print(f"\nProcessing account {uname}:{password}...")

            session = requests.session()
            headers.set_headers(session)
            headers.set_useragent(session)
            proxies.set_proxy(session, pr, i)
            if "cookies" in acc:
                print("Account has cookies, adding them to request and skipping Log In...")
                loggedin=True
                biscuits.load_cookies(session,acc['cookies'])
            else:
                loggedin = fbrequests.login(session, uname, password)

            if not loggedin:
                continue
            token = fbrequests.get_token(session)
            if token == None:
                print("Access Token not found!")
                continue
            print("Found Accesss Token!")
            acc["cookies"] = json.dumps(biscuits.dump_cookies(session.cookies))
            acc["token"] = token
            if use_tinder:
                ttoken = tndr.get_tinder_access_token(session,uname, password)

                if ttoken != None:
                    print("Got Tinder app token...")
                    info = fbrequests.get_acc_info(ttoken)
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
                    f.write(
                        f"{acc['login']}:{acc['password']}:{acc['token']}:{acc['cookies']}\n"
                    )
            else:
                f.write(
                    f"{acc['login']}:{acc['password']}:{acc['token']}:{acc['cookies']}\n"
                )
            i += 1

    print("All done. Accounts with tokens and cookies written to parsed.txt file.")
