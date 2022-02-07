import requests,json
class Proxies:
    @staticmethod
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


    @staticmethod
    def set_proxy(session, proxies, i):
        proxyindex = i if i < len(proxies) - 1 else i % len(proxies)
        cp = proxies[proxyindex]
        pstr=f"http://{cp['login']}:{cp['password']}@{cp['ip']}:{cp['port']}"
        print(f"Using proxy: {pstr}")

        if "link" in cp:
            print("Updating proxy ip address using link...")
            response = requests.get(cp["link"], verify=False)
            if ("Content-Type" in response.headers and response.headers["Content-Type"].startswith("application/json")):
                print("Got response:" + json.dumps(response.text))
            else:
                print("Proxy ip address updated!")
        sproxy = { "https": pstr, "http": pstr}
        session.proxies = sproxy
        return
