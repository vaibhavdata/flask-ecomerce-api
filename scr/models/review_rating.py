from scr.models import db
from scr.shred.MainService import Mainservice
from datetime import datetime,timezone
from marshmallow import Schema, fields

class Review(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'review'
    review_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('public.product.product_id', ondelete='SET NULL'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id', ondelete='SET NULL'), nullable=True)
    review = db.Column(db.String(100),nullable=True)
    rating = db.Column(db.Integer,nullable=False)
    message = db.Column(db.Text,nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.now(), nullable=False)


    def __repr__(self):
        return f'review and rating : {self.review_id}'


    def __init__(self,data):
        self.review_id = data.get('review_id')
        self.product_id = data.get('product_id','')
        self.user_id = data.get('user_id','')
        self.review = data.get('review','')
        self.rating = data.get('rating','')
        self.message = data.get('message','')
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
    def getById(Id):
        try:
            result = Review.query.filter_by(review_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByProductId(Id):
        try:
            result = Review.query.filter_by(product_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserId(Id):
        try:
            result = Review.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

class ReviewSchema(Schema):
    review_id = fields.Int()
    product_id = fields.Int()
    user_id = fields.Int()
    review = fields.Str()
    rating = fields.Int()
    message = fields.Str()
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")


