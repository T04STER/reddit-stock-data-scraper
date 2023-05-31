import logging
from typing import Optional

from models.stock import Stock
from services.yahoo_finance_scraper import YahooFinanceScraper


class StockService:
    def __init__(self, yahoo_scraper: YahooFinanceScraper, drop_collection: bool = False):
        self.__yahoo_scraper = yahoo_scraper
        if drop_collection:
            Stock.drop_collection()

    def get_stock(self, ticker: str) -> Optional[Stock]:
        stock = Stock.objects.filter(ticker=ticker).first()
        if stock is None:
            stock = self.scrap_stock(ticker)
        return stock

    def scrap_stock(self, ticker) -> Optional[Stock]:
        stock = self.__yahoo_scraper.scrap_stock_data(ticker)
        if stock is not None:
            stock_history = self.__yahoo_scraper.scrap_history(ticker)
            stock.stock_history = stock_history
            stock.save()
        return stock

    def get_most_viewed_stocks(self):
        select_params = {
            'ticker': 1,
            'mention_counter': 1,
            'company_name': 1,
            'price': 1,
            'change': 1,
            'change_percent': 1,
            'open_price': 1,
            'previous_close': 1,
            'volume': 1,
        }
        stocks = Stock.objects.only(*select_params).order_by('-mention_counter').limit(10)
        return stocks
