import re

import parsing
import json


def login(session, email, password):
    response = session.get("https://mobile.facebook.com?refsrc=deprecated&_rdr")
    if "cookie/consent_prompt" in response.url:
        inputs, action = parsing.get_form_params(response.text)
        response = session.post(
            f"https://m.facebook.com{action}",
            data=inputs,
            allow_redirects=False,
        )
        if response.status_code == 302:
            location = response.headers["Location"]
            response = session.get(location)
        else:
            raise Exception("Redirect not found!")
        pass

    inputs, action = parsing.get_form_params(response.text)
    email = email.strip()
    password = password.strip()
    params = {
        "email": email,
        "pass": password,
        "login": "Log In",
        "_fb_noscript": False
    }
    inputs.update(params)
    response = session.post(
        f"https://m.facebook.com{action}",
        data=inputs,
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
    print(f"Your account may be disabled! Unknown response: {response.status_code} {response.url}")
    return False


def get_token(session):
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
    session.cookies.pop("noscript", None)
    response = session.get(
        "https://www.facebook.com/ads/manager",
        allow_redirects=True,
    )
    if "checkpoint" in response.url:
        print("Checkpoint!")
        return None
    if "login" in response.url:
        print("Account not logged in!")
        return None
    redirect = parsing.get_redirect(response.text)
    if redirect is not None:
        act = parsing.parse_act(redirect)
        finalUrl = f"https://www.facebook.com/adsmanager/?act={act}&nav_source=no_referrer"
        response = session.get(finalUrl, allow_redirects=True)
        if "privacy/consent/user_cookie_choice" in response.url:
            expId = parsing.parse_experience(response.text)
            uid = parsing.parse_uid(response.text)
            variables = {
                "input": {
                    "client_mutation_id": "2",
                    "actor_id": uid,
                    "config_enum": "USER_COOKIE_CHOICE_FRENCH_CNIL",
                    "experience_id": expId,
                    "extra_params_json": "{}",
                    "flow_name": "USER_COOKIE_CHOICE",
                    "flow_step_type": "STANDALONE",
                    "outcome": "APPROVED",
                    "server_on_complete_params_darray_json": "{\"first_party_trackers_on_foa\":\"true\",\"fb_trackers_on_other_companies\":\"false\",\"other_company_trackers_on_foa\":\"false\"}",
                    "source": "pft_user_cookie_choice",
                    "surface": "FACEBOOK_COMET"
                }
            }
            send_private_api_request(session, 5733973206629812, variables)
            variables = {
                "input": {
                    "client_mutation_id": "3",
                    "actor_id": uid,
                    "config_enum": "USER_COOKIE_CHOICE_FRENCH_CNIL",
                    "experience_id": expId,
                    "extra_params_json": "{}",
                    "flow_name": "USER_COOKIE_CHOICE",
                    "flow_step_type": "STANDALONE",
                    "outcome": "APPROVED",
                    "source": "pft_user_cookie_choice",
                    "surface": "FACEBOOK_COMET"
                }
            }
            send_private_api_request(session, 4943422439028807, variables)
            response = session.get(finalUrl, allow_redirects=True)
        return parsing.parse_token(response.text)
    else:
        return parsing.parse_token(response.text)


def get_acc_info(session, access_token):
    req = session.get(
        f"https://graph.facebook.com/me?scope=email&fields=email,birthday&access_token={access_token}"
    )
    return req.json()


def send_private_api_request(session, docId: int, variables: json) -> json:
    dtsg, lsd, uid = get_private_api_tokens(session)
    body = {
        "av": uid,
        "__user": uid,
        "__a": "1",
        "__comet_req": "0",
        "fb_dtsg": dtsg,
        "lsd": lsd,
        "fb_api_caller_class": "RelayModern",
        "variables": json.dumps(variables),
        "server_timestamps": True,
        "doc_id": str(docId),
    }
    response = session.post("https://www.facebook.com/api/graphql/", data=body)
    return json.loads(response.text)


def get_private_api_tokens(session):
    response = session.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all")
    html = response.text
    match = re.search('DTSGInitialData",\[\],\{"token":"([^"]+)', html)
    dtsg = match.group(1)
    match = re.search('LSD",\[\],\{"token":"([^"]+)', html)
    lsd = match.group(1)
    match = re.search('USER_ID":"(\d+)', html)
    uid = match.group(1)
    return dtsg, lsd, uid
