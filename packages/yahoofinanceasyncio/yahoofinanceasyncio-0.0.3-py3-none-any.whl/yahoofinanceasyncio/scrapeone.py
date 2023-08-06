import numpy as np
import requests
from bs4 import BeautifulSoup


def scrape_yahoo_requests(symbol):
    return parse_yahoo_text(fetch_yahoo_text(symbol))


def yahoo_url(symbol):
    return 'https://finance.yahoo.com/quote/SYMBOL'.replace("SYMBOL",symbol)


def fetch_yahoo_text(symbol):
    url = yahoo_url(symbol=symbol)
    page = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    })
    return page.text


def parse_yahoo_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return float(soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)


if __name__=='__main__':
    y = scrape_yahoo_requests(symbol='IBM')
    print(type(y))