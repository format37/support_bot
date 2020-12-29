#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples/webhook_examples
# https://core.telegram.org/bots/api

import logging
import ssl
from aiohttp import web
import telebot
from telebot import types
import asyncio
import sys
import os
import requests

import urllib.parse
from urllib.parse import urlparse

#SCRIPT_PATH	= '/home/format37_gmail_com/projects/telegram_bot_server/'
SCRIPT_PATH	= '/home/dvasilev/projects/support_bot/'
SSL_PATH = '/etc/letsencrypt/live/service.icecorp.ru/'

#WEBHOOK_HOST = 'www.scriptlab.net'
WEBHOOK_HOST = 'www.service.icecorp.ru'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = SSL_PATH+'fullchain.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = SSL_PATH+'privkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST with www

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

app = web.Application()
bots = []


def default_bot_init(webhook_host, webhook_port, webhook_ssl_cert, script_path):

    with open(script_path+'token.key', 'r') as file:
        api_token = file.read().replace('\n', '')
        file.close()
    bot = telebot.TeleBot(api_token)

    webhook_url_base = "https://{}:{}".format(webhook_host, webhook_port)
    webhook_url_path = "/{}/".format(api_token)

    # Remove webhook, it fails sometimes the set if there is a previous webhook
    bot.remove_webhook()

    # Set webhook
    wh_res = bot.set_webhook(url=webhook_url_base + webhook_url_path, certificate=open(webhook_ssl_cert, 'r'))
    print('webhook set', wh_res)
    print(webhook_url_base + webhook_url_path)

    return bot


# === === === ice ++
bot_script_path = '/home/dvasilev/projects/support_bot/'
idbot = default_bot_init(WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_SSL_CERT, bot_script_path)
bots.append(idbot)


@idbot.message_handler(commands=['user'])
def idbot_user(message):
    idbot.reply_to(message, str(message.from_user.id))
# === === === ice --


# Process webhook calls
async def handle(request):
    for bot in bots:
        if request.match_info.get('token') == bot.token:
            request_body_dict = await request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            bot.process_new_updates([update])
            return web.Response()

    return web.Response(status=403)

app.router.add_post('/{token}/', handle)

# Build ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# Start aiohttp server
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)
