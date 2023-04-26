from app import db


class Stock(db.Document):
    ticker = db.StringField()
    company_name = db.StringField()
    price = db.IntField()
    change = db.IntField()
    change_percent = db.StringField()
    open_price = db.IntField()
    previous_close = db.IntField()
    volume = db.IntField()
