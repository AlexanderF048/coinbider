import ccxt
import asyncio

from src.database.db_connection import session
from src.database.models import CoinBid

import logging

logging.basicConfig(level=logging.INFO)

exchange = ccxt.kucoin()


def create_fake_data(times=12, currency="BTC"):

    for i in range(times):
        session.add(get_bid_ticker(currency))
    session.commit()

    return


def get_bid_ticker(coin: str, exch=exchange):

    Coin = CoinBid(
        currency=exch.fetch_ticker(f'{coin}/USDT')['symbol'],
        price=exch.fetch_ticker(f'{coin}/USDT')['bid']
    )
    logging.info(f"{coin} to USDT now :::>", exch.fetch_ticker(f'{coin}/USDT')['bid'], exch.fetch_ticker(f'{coin}/USDT'))

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

    return output_dict


def coin_list_creator():

    coin_list = []
    for i in exchange.fetch_currencies():
        coin_list.append(i)
    return coin_list


if __name__ == '__main__':

    create_fake_data()

    exit()
