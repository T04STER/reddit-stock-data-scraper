import csv
import io
from http import HTTPStatus

import bs4
import requests
from dot_env_loader import REDDIT_USER_AGENT

class YahooFinanceHistoryScraper:
    __url = r'https://finance.yahoo.com/quote/{0}/history?p={0}'
    __headers = {
        'User-Agent': REDDIT_USER_AGENT
    }

    def scrap_history(self, ticker):
        ticker_url = self.__url.format(ticker)
        response = requests.get(ticker_url, headers=self.__headers)
        if response.status_code != HTTPStatus.OK:
            return None

        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        print(ticker_url)
        download = soup.find("a", {"download": f"{ticker}.csv"})
        download_url = download.get('href')
        response_csv = requests.get(download_url, headers=self.__headers)

        if response_csv.status_code == HTTPStatus.OK:
            raw_csv = response_csv.text
            stock_history = self.__get_stock_history(raw_csv)
            return stock_history
        else:
            return None

    def __get_stock_history(self, raw_csv):
        csv_stream = io.StringIO(raw_csv)
        csv_reader = csv.DictReader(csv_stream)
        stock_history = [{"date": row['Date'], "price": row['Open']} for row in csv_reader]
        return stock_history
