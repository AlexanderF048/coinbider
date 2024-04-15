import asyncio

from aiohttp import web
import requests

from typing import Any, AsyncIterator, Awaitable, Callable, Dict

import json

from router import routes

application = web.Application()


def run_aiohttp_server():
    application.add_routes(routes)
    web.run_app(application)

    return


if __name__ == '__main__':
    run_aiohttp_server()

    exit()
