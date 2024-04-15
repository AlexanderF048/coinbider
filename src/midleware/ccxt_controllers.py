import ccxt
import asyncio
import sys

import pprint
import os

from sqlalchemy import func, select, desc, distinct
from src.database.db_connection import session, Base, engine
from src.database.models import CoinBid

# import ccxt.async_support as ccxt
# print(ccxt.exchanges) # print a list of all available exchange classes
# markets = exchange.load_markets()
# kucoin_ticker = exchange.fetch_ticker(' /USDT')
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

    print(f"{coin} to USDT now :::>", exch.fetch_ticker(f'{coin}/USDT')['bid'], exch.fetch_ticker(f'{coin}/USDT'))

    return Coin


def get_bid_history():
    db_selection = session.query(CoinBid).all()

    for i in db_selection:
        print(f"--{i.time}--{i.id}.{i.currency} ({i.price})")

    return db_selection


def clean_base():
    session.query(CoinBid).delete()
    session.commit()
    return


def get_paginated_bid_history(query=session.query(CoinBid), page=0, page_size=10):
    print('IN PAGINATION')
    print(page)
    if page_size:
        query = query.limit(page_size)
    if page:
        query = query.offset(page * page_size)

    output_dict = {}

    for i in query:
        # print(f"--{i.time}--{i.id}.{i.currency} ({i.price})")
        # print('---------------------------------------------------------------------------------------')
        output_dict[i.id] = {"Currency": i.currency, "Bid": i.price, "Time": i.time.strftime("%H:%M:%S")}
        print('ITERATION')
        print(i)
        print(output_dict[i.id])
    return output_dict


def coin_list_creator():
    coin_list = []

    for i in exchange.fetch_currencies():
        coin_list.append(i)

    return coin_list


if __name__ == '__main__':
    print(coin_list_creator())
    # clean_base()
    # get_bid_history()

    create_fake_data()

    exit()
