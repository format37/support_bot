import asyncio
from aiohttp import web
import urllib
from requests.auth import HTTPBasicAuth
import requests
import json

WEBHOOK_PORT = 8084
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr


async def call_relay(request):
    try:
	script_path = '/home/dvasilev/projects/support_bot/'
        user = urllib.parse.quote_plus(request.rel_url.query['user'])
        text = urllib.parse.quote_plus(request.rel_url.query['text'])
        print(user, text)

        with open(script_path + 'auth.login', 'r') as file:
            login = file.read().replace('\n', '')
            file.close()
        with open(script_path + 'auth.pass', 'r') as file:
            password = file.read().replace('\n', '')
            file.close()

        auth = HTTPBasicAuth(login, password)
        url = "http://10.2.4.123/productionCRM/hs/telegram/api/v1/post/request"

        params = str(user) + '#' + str(text)
        r = requests.post(url, json=json.dumps(params), auth=auth)
        print(r.text)


    except Exception as e:
        print('Error: ' + str(e) )

    return web.Response(text='', content_type="text/html")


app = web.Application()
app.router.add_route('GET', '/relay', call_relay)

web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
)
