from configs import reddit_scraper_config, yahoo_scraper_config
from services.reddit_scraper import RedditScraper
from services.scrap_service import ScrapService
from services.yahoo_finance_scraper import YahooFinanceScraper

yfs = YahooFinanceScraper()
gme = yfs.scrap_stock_data('CNBC')
print(gme)