import os

ANIME_LIST_URL = 'anime-list9.site'

TELEGRAM_BOT_ROOT_URL = 'https://api.telegram.org'

BOT_TOKEN = os.environ.get('BOT_TOKEN')
# print(f'{TELEGRAM_BOT_ROOT_URL}/bot{BOT_TOKEN}/setWebhook')
AJAX_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with': 'XMLHttpRequest',
    'proxy-authorization': 'Basic LnN2QDc3NzE1MDY7aXIuOkdwQksxZkNwQXVGVzYzbFZ1Q3NpaEcvNjNGMFVkaWI3UnlsSjhMSVh5ZzQ9',
}