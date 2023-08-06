from yahoofinanceasyncio.scrapeone import fetch_yahoo_text, parse_yahoo_text, yahoo_url
import aiohttp, asyncio
from getjson import getjson
import numpy as np


def scrape_yahoo_async(symbols):

    async def fetch_pages(session, symbol_url):
        async with session.get(symbol_url) as resp:
            return await resp.text()

    async def fetch_all_pages(symbol_urls, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            return await asyncio.gather(*[fetch_pages(session, symbol_url) for symbol_url in symbol_urls], return_exceptions=True)

    st = time.time()
    symbol_urls = [ yahoo_url(symbol) for symbol in symbols ]
    loop = asyncio.get_event_loop()
    pages = loop.run_until_complete(fetch_all_pages(symbol_urls= symbol_urls, loop=loop))

    fetch_time = time.time()-st
    st = time.time()
    prices = list()
    for symbol, page in zip(symbols, pages):
        try:
            price =  parse_yahoo_text(text=page)
        except:
            print('Parsing failed for '+symbol+' at '+yahoo_url(symbol))
            price = np.nan
        prices.append(price)
    parse_time = time.time()-st
    print({'fetch':fetch_time,'parse':parse_time})
    return prices


if __name__=='__main__':
    symbol_url = 'https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json'
    symbols = getjson(symbol_url).values()
    import time
    st = time.time()
    the_prices = scrape_yahoo_async(symbols=symbols)
    print(the_prices)
    print(time.time()-st)