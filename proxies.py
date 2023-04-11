import requests, json


def get_proxies():
    proxies = []
    pfile = open("proxy.txt", "r")
    plines = pfile.readlines()
    for p in plines:
        linkSplit = p.strip().split("(")
        if len(linkSplit) == 2:
            ps = linkSplit[0].split(":")
            proxies.append(
                {
                    "ip": ps[0],
                    "port": ps[1],
                    "login": ps[2],
                    "password": ps[3],
                    "link": linkSplit[1].strip(')'),
                }
            )
        else:
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
            else:
                raise ValueError("Wrong proxy format!")
    return proxies


def set_proxy(session, proxies, i):
    proxyindex = i if i < len(proxies) - 1 else i % len(proxies)
    cp = proxies[proxyindex]
    pstr = f"http://{cp['login']}:{cp['password']}@{cp['ip']}:{cp['port']}"
    print(f"Using proxy: {pstr}")
    sproxy = {"https": pstr, "http": pstr}
    session.proxies = sproxy
    return


def update_proxy_link(cp):
    if "link" in cp:
        print("Updating proxy ip address using link...")
        response = requests.get(cp["link"], verify=False)
        if "Content-Type" in response.headers and \
                response.headers["Content-Type"].startswith("application/json"):
            print("Got response:" + json.dumps(response.text))
        else:
            print("Proxy ip address updated!")
    return
