from scr.models import db
from scr.shred.MainService import Mainservice
from marshmallow import Schema, fields
import datetime

class PayMethod(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'payMethod'
    payMethod_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.datetime.utcnow())
    userPayMethod = db.relationship('UserPayMethod', backref='public.payMethod', lazy=True)
    order = db.relationship('Order', backref='public.payMethod', lazy=True)
    def __repr__(self):
        return f'Payment method : {self.payMethod_id}'
    def __init__(self,data):
        self.payMethod_id = data.get('payMethod_id')
        self.name = data.get('name','')
        self.date_created = Mainservice.currentDatetime()
        self.updated_at = Mainservice.UpdateDatetime()
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        self.save()

    def save(self):
        #self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getByPaymentId(Id):
        try:
            result = PayMethod.query.filter_by(payMethod_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

class PayMethodSchema(Schema):
    payMethod_id = fields.Int()
    name = fields.String()
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")



