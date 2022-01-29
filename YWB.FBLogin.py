import time, requests, re, json


def copyright():
    print()
    print("               Get Facebook Cookies and Access Token v0.1")
    print("   _            __     __  _ _             __          __  _     ")
    print("  | |           \ \   / / | | |            \ \        / / | |    ")
    print("  | |__  _   _   \ \_/ /__| | | _____      _\ \  /\  / /__| |__  ")
    print("  | '_ \| | | |   \   / _ \ | |/ _ \ \ /\ / /\ \/  \/ / _ \ '_ \ ")
    print("  | |_) | |_| |    | |  __/ | | (_) \ V  V /  \  /\  /  __/ |_) |")
    print("  |_.__/ \__, |    |_|\___|_|_|\___/ \_/\_/    \/  \/ \___|_.__/ ")
    print("          __/ |                                                  ")
    print("         |___/             https://yellowweb.top                 ")
    print()
    print("If you like this script, PLEASE DONATE!")
    print("WebMoney: Z182653170916")
    print("Bitcoin: bc1qqv99jasckntqnk0pkjnrjtpwu0yurm0qd0gnqv")
    print("Ethereum: 0xBC118D3FDE78eE393A154C29A4545c575506ad6B")
    print()
    time.sleep(3)


def get_proxies():
    proxies = []
    pfile = open("proxy.txt", "r")
    plines = pfile.readlines()
    for p in plines:
        ps = p.strip().split(":")
        proxies.append({"ip": ps[0], "port": ps[1], "login": ps[2], "password": ps[3]})
    return proxies


def get_accounts():
    accounts = []
    afile = open("accounts.txt", "r")
    alines = afile.readlines()
    for a in alines:
        acs = a.strip().split(":")
        accounts.append({"login": acs[0], "password": acs[1]})
    return accounts


def login(session, email, password):
    response = session.post(
        "https://m.facebook.com/login.php",
        data={"email": email, "pass": password},
        allow_redirects=False,
    )
    if "checkpoint" in response.headers["Location"]:
        print("Checkpoint!")
        return None
    assert response.status_code == 302
    assert "c_user" in response.cookies
    return response.cookies


def get_token(session, cookies):
    response = session.get("https://fb.com/pe", cookies=cookies, allow_redirects=True)
    match = re.search('window\.location\.replace\("([^"]+)', response.text)
    adsurl = match.group(1).replace("\\", "")
    response = session.get(adsurl, cookies=cookies, allow_redirects=True)
    match = re.search('EAAB[^"]+', response.text)
    if match:
        return match.group(0)
    else:
        return ""


def dump_cookies(sessioncookies):
    cookies = []
    for c in sessioncookies:
        cookies.append(
            {
                "name": c.name,
                "value": c.value,
                "domain": c.domain,
                "path": c.path,
                "expires": c.expires,
            }
        )
    return cookies


if __name__ == "__main__":
    copyright()
    pr = get_proxies()
    accounts = get_accounts()
    i = 0
    with open("parsed.txt", "w") as f:
        for acc in accounts:
            print(f"Processing account {acc['login']}:{acc['password']}...")
            proxyindex = i if i < len(pr) - 1 else i % len(pr)
            cp = pr[proxyindex]
            session = requests.session()
            sproxy = {
                "https",
                f"https://{cp['login']}:{cp['password']}@{cp['ip']}:{cp['port']}",
            }
            session.proxies = sproxy
            cookies = login(session, acc["login"], acc["password"])
            if cookies == None:
                continue
            token = get_token(session, cookies)
            if token != "":
                print("Found token and cookies!")
                acc["cookies"] = dump_cookies(cookies)
                acc["token"] = token
                f.write(
                    f"{acc['login']}:{acc['password']}:{acc['token']}:{acc['cookies']}\n"
                )
            else:
                print("Token and cookies not found(((")
            i += 1

    print("All done. Accounts with tokens and cookies written to parsed.txt file.")
