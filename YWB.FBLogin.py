from requests.packages.urllib3.exceptions import InsecureRequestWarning
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import HardwareType
import time, requests, re, json
from Tinder import Tinder


def copyright():
    print()
    print("               Get Facebook Cookies and Access Token v1.3")
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
        if len(ps) == 4:
            proxies.append(
                {
                    "type": "https",
                    "ip": ps[0],
                    "port": ps[1],
                    "login": ps[2],
                    "password": ps[3],
                }
            )
        elif len(ps) == 5:
            proxies.append(
                {
                    "ip": ps[0],
                    "port": ps[1],
                    "login": ps[2],
                    "password": ps[3],
                    "link": f"http://{ps[4]}",
                }
            )
        elif len(ps) == 6 and (ps[4] == "http" or ps[4] == "https"):
            ulink = f"{ps[4]}:{ps[5]}"
            proxies.append(
                {
                    "ip": ps[0],
                    "port": ps[1],
                    "login": ps[2],
                    "password": ps[3],
                    "link": ulink,
                }
            )
        else:
            raise ValueError("Wrong proxy format!")
    return proxies


def set_proxy(session, proxies, i):
    proxyindex = i if i < len(pr) - 1 else i % len(pr)
    cp = proxies[proxyindex]
    if "link" in cp:

        print("Updating proxy ip address using link...")
        response = requests.get(cp["link"], verify=False)
        if (
            "Content-Type" in response.headers
            and response.headers["Content-Type"].startswith("application/json")
        ):
            print("Got response:" + json.dumps(response.text))
        else:
            print("Proxy ip address updated!")
    sproxy = {
        "https": f"https://{cp['login']}:{cp['password']}@{cp['ip']}:{cp['port']}",
        "http": f"https://{cp['login']}:{cp['password']}@{cp['ip']}:{cp['port']}",
    }
    session.proxies = sproxy
    return


def get_accounts():
    accounts = []
    afile = open("accounts.txt", "r")
    alines = afile.readlines()
    for a in alines:
        acs = a.strip().split(":")
        acc={"login": acs[0], "password": acs[1]}
        match = re.search("\[\s*\{[^\]]+\]", a)  # search for cookies
        if match!=None:
            acc["cookies"]=match.group(0)
        accounts.append(acc)
    return accounts


def login(session, email, password):
    # set our useragent to some mobile phone
    hardware_types = [HardwareType.MOBILE.value]
    user_agent_rotator = UserAgent(hardware_types=hardware_types)
    user_agent = user_agent_rotator.get_random_user_agent()
    session.headers.update({"User-Agent": user_agent})

    email = email.strip()
    password = password.strip()
    response = session.get("https://m.facebook.com")
    # get parameters from login form: lsd, li и m_ts
    match = re.search('name="lsd"\s+value="([^"]+)"', response.text)
    if match == None:
        print("Can't find lsd value!")
        return False
    lsd = match.group(1)
    match = re.search('name="li"\s+value="([^"]+)"', response.text)
    if match == None:
        print("Can't find li value!")
        return False
    li = match.group(1)
    match = re.search('name="m_ts"\s+value="([^"]+)"', response.text)
    if match == None:
        print("Can't find m_ts value!")
        return False
    mts = match.group(1)

    response = session.post(
        "https://m.facebook.com/login/device-based/regular/login/?shbl=1&refsrc=deprecated",
        data={
            "lsd": lsd,
            "m_ts": mts,
            "li": li,
            "try_number": 0,
            "unrecognized_tries": 0,
            "email": email,
            "pass": password,
            "login": "Log In",
            "had_cp_prefilled": False,
            "had_password_prefilled": False,
            "is_smart_lock": False,
            "bi_xrwh": 0,
            "_fb_noscript": True,
        },
        allow_redirects=False,
    )
    if response.status_code == 302:
        if "c_user" in session.cookies:
            print("Logged in!")
            return True

        location = response.headers["Location"]
        if "checkpoint" in location:
            print("Checkpoint!")
            return False
        if "recover" in location or "login" in location:
            print("Wrong login or password!")
            return False
    print(
        f"Your account may be disabled! Unknown response: {response.status_code} {response.url}"
    )
    return False


def parse_token(text):
    match = re.search('EAAB[^"]+', text)
    return match.group(0) if match else None

def get_token(session):
    session.headers.update({"User-Agent": "Mozilla5/0"})
    session.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
    )
    session.headers.update({"Accept-Encoding": "gzip"})
    session.headers.update({"Accept-Language": "ru,en-US;q=0.7,en;q=0.3"})
    session.headers.update({"Connection": "keep-alive"})
    session.headers.update({"Sec-Fetch-Dest": "document"})
    session.headers.update({"Sec-Fetch-Mode": "navigate"})
    session.headers.update({"Sec-Fetch-Site": "same-origin"})
    session.headers.update({"Sec-Fetch-User": "?1"})
    session.cookies.pop("noscript", None)
    response = session.get(
        "https://www.facebook.com/ads/manager?locale=en_US",
        allow_redirects=True,
    )
    if "checkpoint" in response.url:
        print("Checkpoint!")
        return None
    if "login" in response.url:
        print("Account not logged in!")
        return None
    match = re.search('window\.location\.replace\("([^"]+)', response.text)
    if match != None:
        adsurl = match.group(1).replace("\\", "")
        response = session.get(adsurl, allow_redirects=True)
        return parse_token(response.text)
    else:
        return parse_token(response.text)


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
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    copyright()
    tinder = (
        Tinder()
        if input("Do you want to get birthday and email, using Tinder app?(Y/N)") == "Y"
        or "y"
        else None
    )
    pr = get_proxies()
    accounts = get_accounts()
    with open("parsed.txt", "w") as f:
        for i,acc in enumerate(accounts):
            uname = acc["login"]
            password = acc["password"]
            session = requests.session()
            print(f"\nProcessing account {uname}:{password}...")
            set_proxy(session, pr, i)
            if "cookies" in acc:
                print("Account has cookies, adding them to request and skipping Log In...")
                loggedin=True
                jcookies=json.loads(acc['cookies'])
                for jcookie in jcookies:
                    session.cookies.set(jcookie['name'],jcookie['value'],domain=jcookie['domain'])
            else:
                loggedin = login(session, uname, password)

            if not loggedin:
                continue
            token = get_token(session)
            if token != None:
                print("Found Accesss Token!")
                acc["cookies"] = json.dumps(dump_cookies(session.cookies))
                acc["token"] = token
            else:
                print("Token not found!")
                continue
            if tinder != None:
                ttoken = tinder.get_fb_access_token(uname, password)
                if ttoken.startswith("EAA"):
                    print("Got Tinder app token...")
                    info = tinder.get_acc_info(ttoken)
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
