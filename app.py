import re
import json
import requests

from flask import Flask, request, Response, jsonify

from app_config import ANIME_LIST_URL, BOT_TOKEN

from utils import validated_url, initiate_session
from bot import BotAPI

app = Flask(__name__)

@app.route('/home/')
def home():
    print(BOT_TOKEN)
    return 'Hello'

@app.route(f'/{BOT_TOKEN}/', methods=['POST'])
def bot_entry_point():
    req_body = request.data.decode('utf-8')
    json_data = json.loads(req_body)

    print(req_body)

    print(json_data)
    chat_id = json_data['message']['chat']['id']
    input_text = json_data['message']['text']
    if not json_data['message'].get('entities'):
        message_type = 'message'
        text = search_for_anime(input_text)
    else:
        message_type = 'bot_command'
        input_text = input_text.replace('/', '')
        if input_text.isdigit():
            text = get_download_links(input_text)
        elif input_text == 'start':
            text = 'Welcome to Anime List Bot. Try searching for an anime and i will try to find it for you :)'

    try:
        bot_api = BotAPI(chat_id=chat_id)
        bot_api.send_query_result(text)
    except:
        Response("{\"message\": \"bad request\"}", content_type='application/json',status=400)

    return Response("{\"message\": \"ok\"}", content_type='application/json',status=200)

def search_for_anime(search_keyword):
    session = initiate_session()

    data = {
        'type': 'anime',
        '_token': session.cookies.get_dict(ANIME_LIST_URL)['XSRF-TOKEN'],
        's': search_keyword,
    }

    search_url = '{}/front-ajax/ajax-search'.format(ANIME_LIST_URL)
    res = session.post(validated_url(search_url), data=data, verify=False)

    if res:
        search_result = res.json()['res']
        name_pattern = r'<div class="item__title">(.[^<]*)</div>'
        id_pattern = r'<a href="https://anime-list9.site/anime/(\d+)">'
        anime_names = re.findall(name_pattern, search_result)
        anime_ids = re.findall(id_pattern, search_result)
        if anime_ids and anime_names:
            text = ''
            for k, v in zip(anime_names, anime_ids):
                text += '/{id} ==> {name}\n---------------------\n'.format(id=v, name=k)

            text = 'Search Result For: {keyword}\n\n\n{text}'.format(keyword=search_keyword, text=text)
        else:
            text = ''

        return text
    else:
        print(res.text)
        return 'Could not connect to animelist server please try again later!'

def get_download_links(anime_id):
    session = initiate_session()
    links_url = '{}/ajax-dlink/'.format(ANIME_LIST_URL)
    params = {
        'p': anime_id,
        'p2': 2,
    }
    res = session.get(validated_url(links_url), params=params, verify=False)
    if res:
        links_html = res.json()['data']
        link_pattern = r"<a href=[\'\"](.*)[\'\"]>(.[^<]*)<\/a>"
        links = re.findall(link_pattern, links_html)
        print(links)
        if links:
            print(1111111111)
            text = ''
            for link, episode in links:
                text += '{episode}\nLink: {link}\n'.format(episode=episode, link=link)
        else:
            print(22222222)
            text = ''
        
        return text
    else:
        print(res.text)
        return 'Could not connect to animelist server please try again later!'