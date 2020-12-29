import asyncio
from aiohttp import web
import urllib

WEBHOOK_PORT = 8084
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr


async def call_test(request):
    print('ok')
    return web.Response(text='ok', content_type="text/html")


async def call_relay(request):
    try:

        user = urllib.parse.quote_plus(request.rel_url.query['user'])
        text = urllib.parse.quote_plus(request.rel_url.query['text'])
        print(user, text)

    except Exception as e:
        print('Error: ' + str(e) )

    return web.Response(text='', content_type="text/html")


app = web.Application()
app.router.add_route('GET', '/test', call_test)
app.router.add_route('GET', '/relay', call_relay)

web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
)