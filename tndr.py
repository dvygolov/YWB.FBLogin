import re, requests, werkzeug
from requests import sessions

werkzeug.cached_property = werkzeug.utils.cached_property
import robobrowser

def get_tinder_access_token(session):
    url = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id="
    ua = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"
    s = robobrowser.RoboBrowser(session=session, user_agent=ua, parser="html.parser")
    s.open(url)
    f = s.get_form()
    try:
        s.submit_form(f, submit=f.submit_fields["__CONFIRM__"])
        access_token = re.search(
            r"access_token=([\w\d]+)", s.response.content.decode()
        ).groups()[0]
        return access_token
    except requests.exceptions.InvalidSchema as browserAddress:
        access_token = re.search(
            r"access_token=([\w\d]+)", str(browserAddress)
        ).groups()[0]
        return access_token
    except Exception as ex:
        print("Tinder access token could not be retrieved!")
        print("Official error: %s" % ex)
        return None
