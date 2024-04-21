from aiohttp import web
import aiohttp_debugtoolbar
from router import routes

import logging

logging.basicConfig(level=logging.INFO)


async def server_app_factory(router=routes):

    application = web.Application()
    application.add_routes(router)
    aiohttp_debugtoolbar.setup(application)

    return application


if __name__ == '__main__':

    web.run_app(server_app_factory())

    exit()
