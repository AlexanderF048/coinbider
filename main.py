from aiohttp import web
from pathlib import Path
import logging

from db_connection import Base, engine
from midleware.aiohttp_server import server_app_factory

logging.basicConfig(level=logging.INFO)


def main(app=server_app_factory(), db_eng=engine):
    # DB check does 'Coin_bid' exists
    if not db_eng.dialect.has_table(engine.connect(), 'Coin_bid'):
        logging.info(f"NO TABLE 'Coin_bid'")
        Base.metadata.create_all(db_eng)
        Base.metadata.bind = db_eng
        logging.info(f"TABLE 'Coin_bid' CREATED")

    # server run
    web.run_app(app)


if __name__ == '__main__':
    main()

    exit()
