import parsing
def login(session, email, password):
    response = session.get("https://m.facebook.com")
    lsd,jazoest,li,mts,action = parsing.get_login_form_params(response.text)

    email = email.strip()
    password = password.strip()

    response = session.post(
        f"https://m.facebook.com{action}",
        data={
            "lsd": lsd,
            "jazoest": jazoest,
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
    print( f"Your account may be disabled! Unknown response: {response.status_code} {response.url}" )
    return False

def get_token(session):
    session.headers.update({"User-Agent": "Mozilla5/0"})
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
    redirect=parsing.get_redirect(response.text)
    if redirect != None:
        response = session.get(redirect, allow_redirects=True)
        return parsing.parse_token(response.text)
    else:
        return parsing.parse_token(response.text)

def get_acc_info(session,access_token):
    req = session.get(
        f"https://graph.facebook.com/me?scope=email&fields=email,birthday&access_token={access_token}"
    )
    return req.json()
