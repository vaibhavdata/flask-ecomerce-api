from scr.models import db
from scr.shred.MainService import Mainservice
import datetime
from datetime import datetime,timezone
from marshmallow import Schema, fields

class Transaction(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'transaction'
    tran_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    transaction_id = db.Column(db.Integer,nullable=False)
    transaction_data = db.Column(db.JSON(),nullable=True)
    is_success = db.Column(db.Boolean,default=False,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('public.payment.payment_id', ondelete='SET NULL'), nullable=True)

    def __repr__(self):
        return f'transaction: {self.tran_id}'

    def __init__(self, data):
        created_time = Mainservice.currentDatetime()
        self.tran_id = data.get('tran_id')
        self.transaction_id = data.get('transaction_id', '')
        self.transaction_data = data.get('transaction_data','')
        self.is_success = data.get('is_success','')
        self.date_created = created_time
        self.payment_id = data.get('payment_id', '')

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.save()

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def getById(Id):
        try:
            result = Transaction.query.filter_by(tran_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByPaymentId(Id):
        try:
            result = Transaction.query.filter_by(payment_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result


class TranscationSchema(Schema):
    tran_id = fields.Int()
    transaction_id = fields.Int()
    transaction_data = fields.String()
    is_success = fields.Boolean()
    date_created = fields.DateTime()
    payment_id = fields.Int()