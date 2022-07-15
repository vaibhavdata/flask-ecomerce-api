from marshmallow import fields

from scr.models import db, ma
from scr.models.User import UserSchema
from scr.models.cartModel import CartSehema
from scr.models.serviceModel import Product, ProductSchema


class CartItem(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'cartItem'
    cart_item_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('public.cart.cart_id', ondelete='SET NULL'),nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('public.product.product_id', ondelete='SET NULL'),nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id', ondelete='SET NULL'), nullable=True)
    is_active = db.Column(db.Boolean(),default=False,nullable=False)
    quentive = db.Column(db.Integer,nullable=True)
    cart = db.relationship('Cart', backref='public.cartItem',lazy='joined')
    product = db.relationship('Product',backref='public.cartItem',lazy='joined')
    strat_ = db.Column(db.Integer,primary_key=False)

    def __repr__(self):
        return f'Cart items: {self.cart_item_id}'

    def __init__(self,data):
        #self.cart_item_id = data.get('cart_item_id','')
        self.cart_id = data.get('cart_id','')
        self.product_id = data.get('product_id','')
        self.user_id = data.get('user_id','')
        self.is_active = data.get('is_active',False)
        self.quentive = data.get('quentive','')

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        #self.updated_at = datetime.datetime.utcnow()
        self.save()

    def save(self):
        #self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



    @staticmethod
    def getByCartItemId(Id):
        try:
            result = CartItem.query.filter_by(cart_item_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByProductId(Id):
        try:
            result = Product.query.filter_by(product_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByUserId(Id):
        try:
            result = CartItem.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getAll():
        try:
            results = CartItem.query.all()
        except Exception as e:
            results = None
        finally:
            db.session.remove()
        return results


class CartItem_Schema(ma.SQLAlchemySchema):
    cart_item_id = fields.Int()
    is_active = fields.Bool()
    quentive = fields.Int()


    cart = fields.Nested(CartSehema)
    user = fields.Nested(UserSchema)
    product = fields.Nested(ProductSchema)

    class Meta:
        fields =('cart_item_id','is_active','quentive','cart','user','product')



