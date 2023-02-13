import re
from bs4 import BeautifulSoup


# search for cookies
def get_cookies(text):
    match = re.search("\[\s*\{[^\]]+\]", text)
    return match.group(0) if match is not None else None


# get parameters from login form: lsd, li è m_ts
def get_form_params(html):
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.select_one('form')
    inputs = {inpt['name']: inpt['value'] for inpt in form.select('input') if inpt['type'] != 'submit' and inpt.has_attr('value')}
    action = form['action']
    return inputs, action


def parse_token(text):
    match = re.search('EAAB[^"]+', text)
    return match.group(0) if match else None

def parse_uid(text):
    match = re.search('USER_ID":"(\d+)', text)
    return match.group(1) if match else None
def parse_experience(text):
    match = re.search('experience_id":"([^"]+)', text)
    return match.group(1) if match else None

def parse_act(text):
    match = re.search('act=(\d+)', text)
    return match.group(1) if match else None

def get_redirect(text):
    match = re.search('window\.location\.replace\("([^"]+)', text)
    if match is None:
        return None
    redirect = match.group(1).replace("\\", "")
    return redirect
