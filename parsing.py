import re
from html import unescape
class Parsing:
    # search for cookies
    @staticmethod
    def get_cookies(text):
        match = re.search("\[\s*\{[^\]]+\]", text)
        return match.group(0) if match!=None else None

    # get parameters from login form: lsd, li è m_ts
    @staticmethod
    def get_login_form_params(text):
        match = re.search('name="lsd"\s+value="([^"]+)"', text)
        lsd = match.group(1)
        match = re.search('name="jazoest"\s+value="([^"]+)"', text)
        jazoest = match.group(1)
        match = re.search('name="li"\s+value="([^"]+)"', text)
        li = match.group(1)
        match = re.search('name="m_ts"\s+value="([^"]+)"', text)
        mts = match.group(1)
        match = re.search('action="([^"]+)"', text)
        action = unescape(match.group(1))
        return lsd,jazoest,li,mts,action

    @staticmethod
    def parse_token(text):
        match = re.search('EAAB[^"]+', text)
        return match.group(0) if match else None

    def get_redirect(text):
        match = re.search('window\.location\.replace\("([^"]+)', text)
        if match == None:
            return None
        redirect = match.group(1).replace("\\", "")
        return redirect
