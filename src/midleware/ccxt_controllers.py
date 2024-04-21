import ccxt.async_support as ccxt

from src.database.db_connection import session
from src.database.models import CoinBid

import time
import logging

logging.basicConfig(level=logging.INFO)

exchange = ccxt.kucoin()


async def create_fake_data(times=12, currency="BTC"):
    start_time = time.time()
    for i in range(times):
        session.add(await get_bid_ticker(currency))

    session.commit()
    logging.info(f"create_fake_data::FAKEDATA IN BASE: {time.time() - start_time} ")

    return


async def get_bid_ticker(coin: str, exch=exchange):
    start_time = time.time()

    logging.info(f"get_bid_ticker::STARTING:::")

    ticker = await exch.fetch_ticker(f'{coin}/USDT')
    await exch.close()

    logging.info(f"get_bid_ticker::FINISHING WITH TIME: {time.time()-start_time} ")

    Coin = CoinBid(currency=ticker['symbol'], price=ticker['bid'])

    logging.info(f"{coin} to USDT now :::>{ticker['bid'], ticker['timestamp']}")

    return Coin


def get_bid_history():
    db_selection = session.query(CoinBid).all()
    for i in db_selection:
        logging.info(f"--{i.time}--{i.id}.{i.currency} ({i.price})")

    return db_selection


def clean_base():
    session.query(CoinBid).delete()
    session.commit()
    logging.info('BASE CLEAN')

    return


def get_paginated_bid_history(query=session.query(CoinBid), page=0, page_size=10):
    output_dict = {}

    if page_size:
        query = query.limit(page_size)
    if page:
        query = query.offset(int(page) * page_size)

    for i in query:
        output_dict[i.id] = {"Currency": i.currency, "Bid": i.price, "Time": i.time.strftime("%H:%M:%S")}

    logging.info(f"Page:{page} Page size:{page_size}     Items id's:::{output_dict.keys()}")

    return output_dict


async def coin_list_creator(exch=exchange):
    curr_exch = await exch.fetch_currencies()
    await exch.close()

    coin_list = curr_exch.keys()
    logging.info(coin_list)

    return coin_list


if __name__ == '__main__':

    # asyncio.run(create_fake_data())
    # asyncio.run(get_bid_ticker('ETH'))

    exit()
