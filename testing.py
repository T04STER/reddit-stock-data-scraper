from dot_env_loader import REDDIT_SECRET, REDDIT_CLIENT_ID, REDDIT_USER_AGENT
from praw import Reddit

from reddit_scraper.RedditScraper import RedditScrapper
from yahoo_finance_scraper.YahooFinanceHistoryScraper import YahooFinanceHistoryScraper
from yahoo_finance_scraper.YahooFinanceScraper import YahooFinanceScrapper

"""

reddit = Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

srs = ['wallstreetbets']

rs = RedditScrapper(reddit, srs)
rs.scrap()
"""
"""
yfs = YahooFinanceScrapper()
yfs.scrap_stock_data('FRC')
"""
yfhs = YahooFinanceHistoryScraper()
history = yfhs.scrap_history("AAPL")
print(history)