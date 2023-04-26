import logging
import re

import bs4
import requests


class YahooFinanceScrapper:
    __url = r'https://finance.yahoo.com/quote/'

    def scrap_stock_data(self, ticker):
        stock_dict = {}
        ticker_url = f'{self.__url}{ticker}/'
        response = requests.get(ticker_url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string
        company_name = self.__get_company_name(title, ticker)
        if company_name is None:
            logging.warning(f'Not found company with ticker:{ticker}')
            return None

        stock_dict['company_name'] = company_name

        header_div = soup.find('div', id='quote-header-info')
        header_data = self.__get_data_from_header(header_div)
        stock_dict.update(header_data)

        summary_table_div = soup.find('div', {'data-test': 'left-summary-table'})
        table_data = self.__get_data_from_table(summary_table_div)
    def __get_company_name(self, title, ticker):
        pattern = f'(.*?) \\({ticker}\\)'
        match = re.search(pattern, title)
        if match is None:
            return None
        else:
            return match.group(1)

    def __get_data_from_header(self, header_div):
        stock_price = self.__get_atribute_from_header(header_div, 'regularMarketPrice')
        stock_change = self.__get_atribute_from_header(header_div, 'regularMarketPrice')
        stock_change_percent = self.__get_atribute_from_header(header_div, 'regularMarketChangePercent')
        return {
            'stock_price': float(stock_price),
            'stock_change': float(stock_change),
            'stock_change_percent': stock_change_percent
        }

    def __get_atribute_from_header(self, header_div, data_field):
        stock_pattern = {'data-field': data_field}
        stock_data_div = header_div.find('fin-streamer', stock_pattern)
        return stock_data_div.text()

    def __get_data_from_table(self, summary_table):
        # TODO
        return {}

