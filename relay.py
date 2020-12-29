import asyncio
from aiohttp import web

WEBHOOK_PORT = 8084
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr


async def call_test(request):
    return web.Response(text='ok', content_type="text/html")


app = web.Application()
app.router.add_route('GET', '/test', call_test)

web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
)