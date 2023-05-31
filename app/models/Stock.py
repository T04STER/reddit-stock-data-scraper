import mongoengine as me

from models.stock_history_element import StockHistoryElement


class Stock(me.Document):
    ticker = me.StringField(unique=True)
    mention_counter = me.IntField()
    company_name = me.StringField(unique=True)
    price = me.FloatField()
    change = me.FloatField()
    change_percent = me.FloatField()
    open_price = me.FloatField()
    previous_close = me.FloatField()
    volume = me.IntField()
    stock_history = me.ListField(me.EmbeddedDocumentField(StockHistoryElement), default=[])

    # TODO: remove it
    def __repr__(self):
        return f"" \
               f"{self.ticker}" \
               f" ({self.company_name})" \
               f" price {self.price}" \
               f" change {self.change}" \
               f" change percent {self.change_percent}" \
               f" open {self.open_price}" \
               f" prev_close {self.previous_close}" \
               f" volume {self.volume}"
