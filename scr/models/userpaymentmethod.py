from scr.models import db
from scr.shred.MainService import Mainservice
import datetime
from datetime import  datetime,timezone
from marshmallow import Schema, fields

class UserPayMethod(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'user_pay_method'

    userPayMethod_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.now(), nullable=False)
    payMethod_id = db.Column(db.Integer,db.ForeignKey('public.payMethod.payMethod_id',ondelete='SET NULL'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id', ondelete='SET NULL'), nullable=False)
    payment = db.relationship('Payment', backref='public.user_pay_method', lazy=True)
    def __repr__(self):
        return f'user payment method : {self.userPayMethod_id}'

    def __init__(self,data):
        self.userPayMethod_id=data.get('userPayMethod_id')
        self.date_created = Mainservice.currentDatetime()
        self.updated_at = Mainservice.UpdateDatetime()
        self.user_id = data.get('user_id','')
        self.payMethod_id = data.get('payMethod_id','')

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = Mainservice.UpdateDatetime()
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getByPaymethodId(Id):
        try:
            result = UserPayMethod.query.filter_by(payMethod_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserId(Id):
        try:
            result = UserPayMethod.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result
    @staticmethod
    def getById(Id):
        try:
            result = UserPayMethod.query.filter_by(userPayMethod_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result


class UserpayMethod_schema(Schema):
    userPayMethod_id = fields.Int()
    is_delete = fields.Boolean()
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")
    user_id = fields.Int()
    payMethod_id = fields.Int()



