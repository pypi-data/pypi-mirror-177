import yfinance as yf


def yf_price(symbol):
    return yf.Ticker(ticker=symbol).info['regularMarketPrice']


if __name__=='__main__':
    print(yf_price(symbol='IBM'))