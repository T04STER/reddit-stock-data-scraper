from http import HTTPStatus

from flask import typing as ft, jsonify
from flask.views import View

from services.stock_service import StockService


class MostMentionedStockView(View):
    methods = ['GET']

    def __init__(self, stock_service: StockService):
        self.__stock_service = stock_service

    def dispatch_request(self):
        stocks = self.__stock_service.get_most_viewed_stocks()
        if len(stocks) <= 0:
            content = {
                'status': HTTPStatus.NOT_FOUND
            }
            return jsonify(content), HTTPStatus.NOT_FOUND

        return jsonify(stocks), HTTPStatus.OK