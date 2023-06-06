import logging

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_mongoengine import MongoEngine

from configs import reddit_scraper_config, yahoo_scraper_config, aps_scheduler_config
from dot_env_loader import MONGODB_DATABASE, MONGODB_HOSTNAME, MONGODB_USERNAME, MONGODB_PASSWORD
from services.scrap_service import ScrapService
from services.stock_service import StockService
from views.most_mentioned_stocks_view import MostMentionedStockView
from views.stock_view import StockView
from flask_cors import CORS


def init_app():
    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": MONGODB_DATABASE,
            "authentication_source": MONGODB_DATABASE,
            "host": MONGODB_HOSTNAME,
            "port": 27017,
            "alias": "default",
            "username": MONGODB_USERNAME,
            "password": MONGODB_PASSWORD
        }
    ]
    CORS(app, resources={r"/*": {"origins": "*"}}, headers={"Referrer-Policy": "strict-origin-when-cross-origin"})
    reddit_scraper = reddit_scraper_config()
    yahoo_scrapper = yahoo_scraper_config()
    stock_service = StockService(yahoo_scraper_config())
    scrap_service = ScrapService(reddit_scraper, yahoo_scrapper)
    aps_scheduler_config(scrap_service)

    app.add_url_rule('/api/v1/stocks/<ticker>', view_func=StockView.as_view('stock_view', stock_service))
    app.add_url_rule(
        '/api/v1/stocks/',
        view_func=MostMentionedStockView.as_view('most_mentioned_stocks_view', stock_service)
    )
    return app


db = MongoEngine()
app = init_app()
db.init_app(app)

