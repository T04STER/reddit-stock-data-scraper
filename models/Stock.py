from app import db


class Stock(db.Document):
    ticker = db.StringField()
    mention_counter = db.IntField()
    company_name = db.StringField()
    price = db.FloatField()
    change = db.FloatField()
    change_percent = db.StringField()
    open_price = db.FloatField()
    previous_close = db.FloatField()
    volume = db.IntField()
    # TODO remove it:
    def __str__(self):
        return f"{self.ticker} ({self.company_name}) {self.price} {self.change} {self.change_percent} open: {self.open_price}"
