import requests

from app_config import ANIME_LIST_URL, AJAX_HEADERS

validated_url = lambda url: url if url.startswith('http') else ('https://' + url)

def format_cookies(cookie_jar):
    cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)
    found = ['%s=%s' % (name, value) for (name, value) in cookie_dict.items()]
    return ';'.join(found)

def initiate_session():
    cookies = requests.get(validated_url(ANIME_LIST_URL), verify=False).cookies

    session = requests.Session()

    # Set cookies
    session.cookies = cookies
    session.cookies.set('zpv0', '1', domain=ANIME_LIST_URL)
    session.cookies.set('size_window', '0', domain=ANIME_LIST_URL)

    # Set headers
    session.headers = AJAX_HEADERS
    session.headers.update({'cookie': format_cookies(session.cookies)})
    return session