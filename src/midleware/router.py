from aiohttp import web

from ccxt_controllers import get_bid_ticker, get_paginated_bid_history, clean_base, coin_list_creator
from db_connection import session

routes = web.RouteTableDef()


# http://0.0.0.0:8080/price/history/?page=<pagenum>
@routes.get('/price/history', name='history')
async def get_history_pagination(request):
    try:
        page_num = request.rel_url.query.get("page")
        response_obj = get_paginated_bid_history(page=page_num)

        return web.json_response(response_obj)

    except Exception as error:
        return web.Response(status=404, text=str(error))


# http://0.0.0.0:8080/price/history/kill
@routes.delete('/price/history/kill', name='delete')
async def delete_bids_history(request):
    try:
        clean_base()
        return web.Response(status=200, text="BASE DELETED SUCCESSFULLY")

    except Exception:
        return web.Response(status=400, text="Page Not Found")


# http://0.0.0.0:8080/price/BTC <or currency you want to download>
@routes.get('/price/{currency}', name='bid')
def get_bid(request):
    resp_curr = request.match_info['currency']

    if resp_curr in coin_list_creator():

        try:
            curr_obj = get_bid_ticker(resp_curr)

            session.add(curr_obj)
            session.commit()

            return web.Response(status=201, text="CREATED (NEW RAW IN BASE)")

        except Exception as error:
            return web.Response(status=404, text=str(error))
    else:
        return web.Response(status=400, text="Try again Not Found")
