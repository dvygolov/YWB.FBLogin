import json

def load_cookies(session,cookies):
    jcookies=json.loads(cookies)
    for jcookie in jcookies:
        session.cookies.set(jcookie['name'],jcookie['value'],domain=jcookie['domain'])

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
