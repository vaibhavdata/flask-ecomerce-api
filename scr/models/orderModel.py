from scr.models import db
from scr.shred.MainService import Mainservice
from marshmallow import Schema, fields
import datetime

class Order(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'order'

    order_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    #product_id = db.Column(db.Integer, db.ForeignKey('public.product.product_id', ondelete='SET NULL'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id', ondelete='SET NULL'), nullable=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('public.payment.payment_id', ondelete='SET NULL'), nullable=True)
    order_number = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    address_1 = db.Column(db.String(200),nullable=False)
    address_2 = db.Column(db.String(200),nullable=False)
    city = db.Column(db.String(250), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    order_note = db.Column(db.String(250),nullable=True)
    amount = db.Column(db.Integer,nullable=False)
    tex = db.Column(db.Integer,nullable=True)
    ip_address = db.Column(db.String(50),nullable=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('public.product_plans.plan_id', ondelete='SET NULL'), nullable=True)
    payMethod_id = db.Column(db.Integer, db.ForeignKey('public.payMethod.payMethod_id', ondelete='SET NULL'), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.datetime.utcnow())
    #offer_id = db.Column(db.Integer, db.ForeignKey('public.product_offer.offer_id', ondelete='SET NULL'), nullable=True)

    def __repr__(self):
        return f'order : {self.payMethod_id}'

    def __init__(self,data):
        created_date = Mainservice.currentDatetime()
        update_date = Mainservice.UpdateDatetime()
        self.order_id = data.get('order_id')
        self.user_id = data.get('user_id','')
        self.payment_id = data.get('payment_id','')
        self.order_number = data.get('order_number','')
        self.email  = data.get('email', '')
        self.first_name  = data.get('first_name', '')
        self.last_name  = data.get('last_name', '')
        self.address_1  = data.get('address_1', '')
        self.address_2  = data.get('address_2', '')
        self.city = data.get('city','')
        self.zip_code  = data.get('zip_code', '')
        self.state  = data.get('state', '')
        self.country = data.get('country', '')
        self.order_note  = data.get('order_note', '')
        self.amount = data.get('amount', '')
        self.tex  = data.get('tex', '')
        self.ip_address  = data.get('ip_address', '')
        self.plan_id = data.get('plan_id', '')
        self.payMethod_id = data.get('payMethod_id', '')
        self.date_created = created_date
        self.updated_at = update_date

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getById(Id):
        try:
            result = Order.query.filter_by(order_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserId(Id):
        try:
            result = Order.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByPaymentId(Id):
        try:
            result = Order.query.filter_by(payment_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

class OrderSchema(Schema):
    order_id = fields.Int()
    user_id = fields.Int()
    payment_id = fields.Int()
    order_number = fields.Str()
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    address_1 = fields.Str()
    address_2 = fields.Str()
    city = fields.Str()
    zip_code = fields.Str()
    state = fields.Str()
    country = fields.Str()
    order_note = fields.Str()
    amount = fields.Int()
    tex = fields.Int()
    ip_address = fields.Str()
    plan_id = fields.Int()
    payMethod_id = fields.Int()
    date_created = fields.DateTime()
    updated_at = fields.DateTime()




