from scr.models import db
from scr.shred.MainService import Mainservice
import datetime
from datetime import datetime, timezone
from marshmallow import Schema, fields
from scr.models.User import UserSchema


class Cart(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id'), unique=True, nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.now(),
                           nullable=False)

    user = db.relationship('User', backref='public.user', lazy='joined')

    def __repr__(self):
        return f'Cart : {self.cart_id}'

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.date_created = Mainservice.currentDatetime()
        self.updated_at = Mainservice.UpdateDatetime()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.save()

    def save(self):
        # self.date_created = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getById(Id):
        try:
            result = Cart.query.filter_by(cart_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserId(Id):
        try:
            result = Cart.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getAll():
        try:
            results = Cart.query.order_by(Cart.user_id.desc()).all()
        except Exception as e:
            results = None
        finally:
            db.session.remove()
        return results


class CartSehema(Schema):
    cart_id = fields.Int()
    user = fields.Nested(UserSchema(only=("user_id",)))
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")
