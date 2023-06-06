import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from praw import Reddit
from tzlocal import get_localzone

from dot_env_loader import REDDIT_CLIENT_ID, REDDIT_SECRET, \
    REDDIT_USER_AGENT
from services.reddit_scraper import RedditScraper
from services.scrap_service import ScrapService
from services.yahoo_finance_scraper import YahooFinanceScraper


def reddit_scraper_config():
    reddit_client = Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET,
            user_agent=REDDIT_USER_AGENT
    )
    subreddits_sources = ["wallstreetbets", 'stocks']
    post_limit = 20
    reddit_scrapper = RedditScraper(reddit_client, subreddits_sources, post_limit)
    return reddit_scrapper


def aps_scheduler_config(scrap_service: ScrapService):
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.configure(timezone=get_localzone())
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scraping_start_date = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(
        scrap_service.insert_most_mentioned_stocks,
        'interval',
        hours=12,
        id='1',
        name='get_and_insert_stocks',
        start_date=scraping_start_date
    )
    update_start_date = datetime.now() + timedelta(hours=2)

    scheduler.add_job(
        scrap_service.update_stock_data,
        'interval',
        hours=2,
        id='2',
        name='update_existing_stocks',
        start_date=update_start_date
    )
    scheduler.start()
    scheduler.print_jobs()


def yahoo_scraper_config():
    yfs = YahooFinanceScraper()
    return yfs

