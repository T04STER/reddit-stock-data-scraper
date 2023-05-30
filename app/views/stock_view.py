from http import HTTPStatus
from typing import Tuple

from flask import jsonify
from flask.views import View
from flask import Response
from models import Stock
from services.stock_service import StockService


class StockView(View):
    methods = ['GET']

    def __init__(self, stock_service: StockService):
        self.__stock_service: StockService = stock_service

    def dispatch_request(self, ticker: str) -> Tuple[Response, HTTPStatus]:
        stock = self.__stock_service.get_stock(ticker)
        if stock is None:
            content = {
                'status': HTTPStatus.NOT_FOUND,
                'message': "Couldn't find stock neither in database nor on yahoo"
            }
            return jsonify(content), HTTPStatus.NOT_FOUND
        return jsonify(stock), HTTPStatus.OK
