import csv
import io
import logging
import re
from http import HTTPStatus
from typing import Optional, Dict, List, Union
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
        if response.status_code != HTTPStatus.OK:
            logging.warning(f"Request status {response.status_code}")
            return None

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

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

    def __get_data_from_header(self, header_div) -> Dict:
        stock_price = self.__extract_value_in_fin_streamer(header_div, 'regularMarketPrice')
        stock_change = self.__extract_value_in_fin_streamer(header_div, 'regularMarketChange')
        stock_change_percent = self.__extract_value_in_fin_streamer(header_div, 'regularMarketChangePercent')
        if stock_change_percent is not None:
            stock_change_percent *= 100

        return {
            'price': stock_price,
            'change': stock_change,
            'change_percent': stock_change_percent
        }

    def __extract_value_in_fin_streamer(self, header_div, data_field) -> Optional[Union[int, float]]:
        data_field_pattern = {'data-field': data_field}
        fin_streamer = header_div.find('fin-streamer', data_field_pattern)

        if fin_streamer is None:
            return None
        value = fin_streamer.get('value')
        value = self.__parse_to_number(value)
        return value

    def __get_data_from_table(self, summary_table) -> Dict:
        # TODO!!!: TEST IT!!!
        table_cell = 'td'

        open_price_search_param = {'data-test': 'OPEN-value'}
        open_price = self.__extract_number_from_div(summary_table, table_cell, open_price_search_param)

        prev_close_search_param = {'data-test': 'PREV_CLOSE-value'}
        previous_close = self.__extract_number_from_div(summary_table, table_cell, prev_close_search_param)

        volume = self.__extract_value_in_fin_streamer(summary_table, 'regularMarketVolume')

        return {
            'open_price': open_price,
            'previous_close': previous_close,
            'volume': volume
        }

    def __extract_number_from_div(self, div, value_container_name, search_param) -> Optional[Union[int, float]]:
        element_container = div.find(value_container_name, search_param)
        if element_container is None:
            return None

        element = element_container.text
        return self.__parse_to_number(element)

    def __parse_to_number(self, text) -> Optional[Union[int, float]]:
        text = text.replace(',', '')
        only_digit_text = text.replace('.', '')
        if only_digit_text[0] == '-':
            only_digit_text = only_digit_text[1:]

        if not only_digit_text.isdigit():
            return None

        if text == only_digit_text:
            return int(text)
        else:
            return float(text)

    def scrap_history(self, ticker: str) -> List[StockHistoryElement]:
        ticker_url: str = self.__history_url.format(ticker)
        response = requests.get(ticker_url, headers=self.__headers)

        if response.status_code != HTTPStatus.OK:
            return list()

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        download = soup.find('a', {'download': f"{ticker}.csv"})
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
