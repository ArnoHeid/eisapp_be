from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

ICE_PRICE = 0.6


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    nfcid = db.Column(db.String(80), unique=True, nullable=False)
    amount = db.Column(db.Float, unique=True, nullable=False)

    def __init__(self, nfcid):
        self.nfcid = nfcid


    def create_json(self, do_update=False):
        response_json = json.dumps({
            'name': self.username,
            'nfcid': self.nfcid,
            'amount': self.amount,
            'isok': self.check_amount_and_reduce() if do_update else False
        })
        return response_json

    def check_amount_and_reduce(self):
        if self.amount < ICE_PRICE:
            return False
        else:
            self.amount = self.amount - ICE_PRICE
            db.session.commit()
            return True
