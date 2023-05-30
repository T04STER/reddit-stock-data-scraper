import csv
import io
import logging
import re
from http import HTTPStatus
from typing import Optional, Dict, List
import bs4
import requests

from dot_env_loader import REDDIT_USER_AGENT
from models.stock import Stock
from models.stock_history_element import StockHistoryElement


class YahooFinanceScraper:
    __url = r'https://finance.yahoo.com/quote/'
    __history_url = r'https://finance.yahoo.com/quote/{0}/history?p={0}'
    __headers = {
        'User-Agent' : f'{REDDIT_USER_AGENT}',
    }

    def scrap_stock_data(self, ticker) -> Optional[Stock]:
        stock_dict = {"ticker": ticker}
        ticker_url = f'{self.__url}{ticker}/'
        response = requests.get(ticker_url, headers=self.__headers)

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        if response.status_code != HTTPStatus.OK:
            logging.warning(f"Request status {response.status_code}")
            return None

        title = soup.title.string
        company_name = self.__get_company_name(title, ticker)

        if company_name is None:
            logging.warning(f'Not found company with ticker: {ticker}')
            return None

        stock_dict['company_name'] = company_name

        header_div = soup.find('div', id='quote-header-info')
        header_data = self.__get_data_from_header(header_div)
        stock_dict.update(header_data)

        summary_table_div = soup.find('div', {'data-test': 'left-summary-table'})
        table_data = self.__get_data_from_table(summary_table_div)
        stock_dict.update(table_data)
        return Stock(**stock_dict)

    def __get_company_name(self, title: str, ticker: str) -> Optional[str]:
        pattern = r'(.*?) \({0}\)'.format(ticker)
        match = re.search(pattern, title)
        if match is None:
            return None
        else:
            return match.group(1)

    def __get_data_from_header(self, header_div: str) -> Dict:
        stock_price = self.__get_atribute_from_header(header_div, 'regularMarketPrice')
        stock_change = self.__get_atribute_from_header(header_div, 'regularMarketPrice')
        stock_change_percent = self.__get_atribute_from_header(header_div, 'regularMarketChangePercent')
        return {
            'price': float(stock_price),
            'change': float(stock_change),
            'change_percent': float(stock_change_percent)*100
        }

    def __get_atribute_from_header(self, header_div, data_field):
        stock_pattern = {'data-field': data_field}
        stock_data_div = header_div.find('fin-streamer', stock_pattern)
        print(stock_data_div)

        return stock_data_div.get('value', 0)

    def __get_data_from_table(self, summary_table):
        # TODO:
        return {}

    def scrap_history(self, ticker: str) -> List[StockHistoryElement]:
        ticker_url: str = self.__history_url.format(ticker)
        response = requests.get(ticker_url, headers=self.__headers)

        if response.status_code != HTTPStatus.OK:
            return list()

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
            return list()

    def __get_stock_history(self, raw_csv: str) -> List[StockHistoryElement]:
        csv_stream = io.StringIO(raw_csv)
        csv_reader = csv.DictReader(csv_stream)
        stock_history = [StockHistoryElement(date=row['Date'], price=row['Open']) for row in csv_reader]

        return stock_history
