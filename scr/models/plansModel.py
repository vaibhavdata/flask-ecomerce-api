from scr.models import db
from scr.shred.MainService import Mainservice
import datetime
from datetime import datetime,timezone
from marshmallow import Schema, fields

class PlanModel(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'product_plans'

    plan_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100))
    price =  db.Column(db.Integer)

    is_type = db.Column(db.Boolean,nullable=True)
    is_active = db.Column(db.Boolean ,default=True ,nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.now(), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('public.product.product_id', ondelete='SET NULL'),nullable=True)
    order  = db.relationship('Order', backref='public.product_plans', lazy=True)
    payment = db.relationship('Payment', backref='public.product_plans', lazy=True)
    def __repr__(self):
        return f'product plans: {self.plan_id}'
    def __init__(self,data):
        created_date = Mainservice.currentDatetime()
        update_at = Mainservice.UpdateDatetime()
        self.plan_id = data.get('plan_id')
        self.name = data.get('name','')
        self.price = data.get('price','')
        self.is_type = data.get('is_type','')
        self.is_active = data.get('is_active',True)
        self.date_created = created_date
        self.updated_at = update_at
        self.product_id = data.get('product_id','')
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
    def getById(Id):
        try:
            result = PlanModel.query.filter_by(plan_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByProductId(Id):
        try:
            result = PlanModel.query.filter_by(product_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

class PlanSchema(Schema):
    plan_id = fields.Int()
    name = fields.Str()
    price = fields.Int()
    is_type = fields.Boolean()
    is_active = fields.Boolean()
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")
    product_id = fields.Int()





