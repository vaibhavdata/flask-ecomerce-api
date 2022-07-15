from scr.models import db
from scr.shred.MainService import Mainservice
from datetime import datetime,timezone
from marshmallow import Schema, fields





class Payment(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), default=0)
    is_payment = db.Column(db.Boolean,default=False,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.now(), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('public.product_plans.plan_id', ondelete='SET NULL'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('public.product.product_id', ondelete='SET NULL'), nullable=True)
    user_id =db.Column(db.Integer, db.ForeignKey('public.user.user_id', ondelete='SET NULL'), nullable=True)
    userPayMethod_id = db.Column(db.Integer, db.ForeignKey('public.user_pay_method.userPayMethod_id', ondelete='SET NULL'), nullable=True)
    #transaction = db.relationship('Transaction', backref='public.payment', lazy=True)
    order =  db.relationship('Order', backref='public.payment', lazy=True)



    def __repr__(self):
        return f'payment : {self.payment_id}'
    def __init__(self,data):
        created_time = Mainservice.currentDatetime()
        update_time = Mainservice.UpdateDatetime()
        self.payment_id = data.get('payment_id')
        self.amount = data.get('amount','')
        self.is_payment = data.get('is_payment',False)
        self.date_created = created_time
        self.updated_at = update_time
        self.plan_id = data.get('plan_id','')
        self.product_id = data.get('product_id','')
        self.user_id = data.get('user_id','')
        self.userPayMethod_id = data.get('userPayMethod_id','')

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
    def getById(Id):
        try:
            result = Payment.query.filter_by(payment_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByPlanId(Id):
        try:
            result = Payment.query.filter_by(plan_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByProductId(Id):
        try:
            result = Payment.query.filter_by(product_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserId(Id):
        try:
            result = Payment.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserPayMethId(Id):
        try:
            result = Payment.query.filter_by(userPayMethod_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

class PaymentSchema(Schema):
    payment_id = fields.Int()
    amount = fields.Float()
    is_payment = fields.Boolean()
    date_created = fields.DateTime()
    updated_at = fields.DateTime()
    plan_id = fields.Int()
    product_id = fields.Int()
    user_id = fields.Int()
    userPayMethod_id = fields.Int()





