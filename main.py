

from aiohttp import web
import asyncio

from aiohttp_server import run_aiohttp_server
from ccxt_controllers import coin_list_creator

from db_connection import Base, engine

from midleware.aiohttp_server import run_aiohttp_server
def main():

    #server run 
    run_aiohttp_server()
    
    #ccxt
    coin_list = coin_list_creator()

    #DB
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine  

    return

if __name__ == '__main__':

    main()

    exit()