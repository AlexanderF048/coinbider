import json
from aiohttp import web

from ccxt_controllers import get_bid_ticker, get_paginated_bid_history, clean_base
from db_connection import session

routes = web.RouteTableDef()


# http://0.0.0.0:8080/price/history/?page=<pagenum>
@routes.get('/price/history', name='history')
def get_history_pagination(request):
    print("hello im in history")
    page_num = request.rel_url.query.get("page")


    response_obj = get_paginated_bid_history(page=page_num)

    #return web.Response(status=200, text="HISTORY WITH PAGINATION")
    return web.json_response(response_obj)


# http://0.0.0.0:8080/price/history/kill
@routes.delete('/price/history/kill', name='delete')
def delete_bids_history(request):
    clean_base()
    return web.Response(status=200, text="BASE DELETED SUCCESSFULLY")


# http://0.0.0.0:8080/price/BTC <or currency you want to download>
@routes.get('/price/{currency}', name='bid')
def get_bid(request):
    resp_curr = request.match_info['currency']

    curr_obj = get_bid_ticker(resp_curr)

    session.add(curr_obj)
    session.commit()

    return web.Response(status=200, text="ADDED NEW RAW IN BASE")
