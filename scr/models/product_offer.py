from scr.models import db
from scr.shred.MainService import Mainservice
import datetime
from datetime import datetime,timezone
from marshmallow import Schema, fields

class OfferOnPro(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'product_offer'
    offer_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100))
    description = db.Column(db.Text,nullable=True)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    is_flat = db.Column(db.Boolean,nullable=True)
    discount_amount = db.Column(db.Integer)
    discount_percen = db.Column(db.Integer)
    is_free = db.Column(db.Boolean,default=False,nullable =True)
    duration_months = db.Column(db.Integer,nullable=True)
    duration_end_date = db.Column(db.DateTime(timezone=True),nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id', ondelete='SET NULL'), nullable=True)
    #order = db.relationship('Order', backref='public.product_offer', lazy=True)
    def __repr__(self):
        return f'offer on product : {self.offer_id}'


    def __init__(self,data):
        self.offer_id = data.get('offer_id')
        self.name = data.get('name','')
        self.description = data.get('description','')
        self.start_date = data.get('start_date','')
        self.end_date = data.get('end_date','')
        self.is_flat = data.get('is_flat','')
        self.discount_amount = data.get('discount_amount','')
        self.discount_percen = data.get('discount_percen','')
        self.is_free = data.get('is_free',False)
        self.duration_months = data.get('duration_months','')
        self.duration_end_date = data.get('duration_end_date','')
        self.user_id = data.get('user_id','')
        self.date_created = Mainservice.currentDatetime()
        self.updated_at = Mainservice.UpdateDatetime()

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
            result = OfferOnPro.query.filter_by(offer_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserId(Id):
        try:
            result = OfferOnPro.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

class OfferSchema(Schema):
    offer_id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    is_flat = fields.Boolean()
    discount_amount = fields.Int()
    discount_percen = fields.Int()
    is_free = fields.Boolean()
    duration_months = fields.Int()
    duration_end_date = fields.DateTime()
    date_created = fields.DateTime()
    updated_at = fields.DateTime()







