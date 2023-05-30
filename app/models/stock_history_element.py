import mongoengine as me


class StockHistoryElement(me.EmbeddedDocument):
    date = me.DateField()
    price = me.FloatField()
