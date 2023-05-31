from typing import List
from models import Stock
from models.stock_history_element import StockHistoryElement
from services.reddit_scraper import RedditScraper
from services.yahoo_finance_scraper import YahooFinanceScraper


class ScrapService:
    def __init__(self, reddit_scraper: RedditScraper, yahoo_finance_scraper: YahooFinanceScraper):
        self.__reddit_scraper: RedditScraper = reddit_scraper
        self.__yahoo_finance_scraper: YahooFinanceScraper = yahoo_finance_scraper

    def insert_most_mentioned_stocks(self) -> None:
        most_mentioned: List = self.__reddit_scraper.scrap()
        stocks = self.__scrap_stocks_data(most_mentioned)
        for stock in stocks:
            existing_stock = Stock.objects(ticker=stock.ticker)
            if existing_stock is not None:
                existing_stock.update(
                    price=stock.price,
                    change=stock.change,
                    mention_counter=stock.mention_counter,
                    change_percent=stock.change_percent,
                    open_price=stock.open_price,
                    previous_close=stock.previous_close,
                    volume=stock.volume,
                    stock_history=stock.stock_history
                )
            else:
                stock.save()

    def update_stock_data(self) -> None:
        for stock in Stock.objects:
            new_stock = self.__yahoo_finance_scraper.scrap_stock_data(stock.ticker)
            if new_stock is not None:
                new_stock_history = self.__yahoo_finance_scraper.scrap_history(stock.ticker)
                if len(new_stock_history) > 0:
                    new_stock.stock_history = new_stock_history

                stock.update(
                    price=new_stock.price,
                    change=new_stock.change,
                    change_percent=new_stock.change_percent,
                    open_price=new_stock.open_price,
                    previous_close=new_stock.previous_close,
                    volume=new_stock.volume,
                    stock_history=new_stock.stock_history
                )

    def __scrap_stocks_data(self, most_mentioned: List) -> List[Stock]:
        stocks = list()
        for (ticker, mentions) in most_mentioned:
            stock = self.__yahoo_finance_scraper.scrap_stock_data(ticker)
            if stock is not None:
                stock.mention_counter = mentions

                stock_history: List[StockHistoryElement] = self.__yahoo_finance_scraper.scrap_history(ticker)
                stock.stock_history = stock_history
                stocks.append(stock)
        return stocks

