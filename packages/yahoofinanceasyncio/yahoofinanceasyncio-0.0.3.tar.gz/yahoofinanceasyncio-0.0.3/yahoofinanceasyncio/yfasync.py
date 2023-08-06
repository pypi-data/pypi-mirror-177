from yahoofinanceasyncio.scrapeone import fetch_yahoo_text, parse_yahoo_text, yahoo_url
import aiohttp, asyncio
from getjson import getjson
import numpy as np
from yahoofinanceasyncio.yfin import yf_price

# I don't expect this to work :)


def yf_async(symbols):

    async def fetch_price(symbol):
        return await yf_price(symbol=symbol)

    async def fetch_all_prices(symbols, loop):
        return await asyncio.gather(*[fetch_price(symbol) for symbol in symbols], return_exceptions=True)

    st = time.time()
    loop = asyncio.get_event_loop()
    prices = loop.run_until_complete(fetch_all_prices(symbols= symbols, loop=loop))
    fetch_time = time.time()-st
    print({'fetch':fetch_time})
    return prices


if __name__=='__main__':
    symbol_url = 'https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json'
    symbols = getjson(symbol_url).values()
    import time
    st = time.time()
    prices = yf_async(symbols=symbols)
    print(time.time()-st)