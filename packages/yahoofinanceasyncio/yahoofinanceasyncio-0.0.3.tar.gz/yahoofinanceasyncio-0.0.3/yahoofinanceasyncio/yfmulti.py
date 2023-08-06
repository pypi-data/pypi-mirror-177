from yahoofinanceasyncio.scrapeone import fetch_yahoo_text, parse_yahoo_text, yahoo_url
import aiohttp, asyncio
from getjson import getjson
import numpy as np
from yahoofinanceasyncio.yfin import yf_price
from multiprocessing import Pool
import time

# I don't expect this to work :)


def yf_multi(symbols):
    st = time.time()
    pool = Pool()
    prices = pool.map( yf_price, symbols )
    fetch_time = time.time()-st
    print({'fetch':fetch_time})
    return prices


if __name__=='__main__':
    symbol_url = 'https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json'
    symbols = getjson(symbol_url).values()
    yf_multi(symbols=symbols)