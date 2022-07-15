from scr.models import db,ma
from scr.shred.MainService import Mainservice,Label
import datetime
from scr.models.categoryModel import CategorySchema,Category
from marshmallow import Schema, fields
from scr.shred.paginationSechema import PaginationSchema
from marshmallow import Schema, fields
from urllib.parse import urlencode
class Product(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'product'

    product_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    product_name = db.Column(db.String(100))
    product_slug = db.Column(db.String(100))
    #image = db.Column(ARRAY(JSON), nullable=True)
    is_delete = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Integer,nullable=True)
    old_price = db.Column(db.Integer,nullable=True)
    #label = db.Column(db.Enum(Label,values_callable=lambda x: [str(label.value) for label in Label]))
    item_stock = db.Column(db.Integer,nullable=True)
    is_plan = db.Column(db.Boolean,default=False, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('public.category.category_id',ondelete='SET NULL'),nullable=True)
    #user_id = db.Column(db.Integer,db.ForeignKey('public.user.user_id',ondelete='SET NULL'),nullable=True)
    #reivew = db.relationship('Review', backref='public.product', lazy=True)
    category =db.relationship('Category', backref='public.product')

    def __repr__(self):
        return f'product : {self.product_id}'

    def __init__(self,data):
        self.product_id = data.get('product_id')
        self.product_name = data.get('product_name','')
        self.product_slug = data.get('product_slug','')
        #self.image = data.get('image','')
        self.is_delete = data.get('is_delete',False)
        self.price = data.get('price','')
        self.old_price = data.get('old_price','')
        #self.label = data.get('label','')
        self.item_stock = data.get('item_stock','')
        self.is_plan = data.get('is_plan','')
        self.date_created = Mainservice.currentDatetime()
        self.updated_at = Mainservice.UpdateDatetime()
        self.category_id = data.get('category_id', '')
        #self.user_id = data.get('user_id','')




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

    def getById(Id):
        try:
            result = Product.query.filter_by(product_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByIsdeleteId(Id):
        try:
            result = Product.query.filter_by(product_id=Id,is_delete =True).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getAll():
        try:
            results = Product.query.order_by(Product.id_user.desc()).all()
        except Exception as e:
            results = None
        finally:
            db.session.remove()
        return results



class ProductSchema(ma.SQLAlchemySchema):
    category =  fields.Nested(CategorySchema(only=("name","category_id",)))
    #category = fields.Pluck(CategorySchema, 'name')
    product_name = fields.Str()
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")
    is_delete = fields.Boolean()
    price = fields.Int()
    item_stock = fields.Int()

class PaginationSchema(ma.SQLAlchemySchema):
    page = fields.Integer(missing=1)
    per_page = fields.Integer(data_key='perPage', missing=10)
    total = fields.Integer()
    product_name = fields.Str()
    price = fields.Int()
    item_stock = fields.Int()
    pages = fields.Integer(data_key='totalPages')
    has_next = fields.Boolean(data_key='hasNext')
    has_prev = fields.Boolean(data_key='hasPrev')



    '''def get_product(self, obj):
        data = Product.query.filter_by(product_name=ob).first()
        departmentSchema = ProductSchema()
        departmentSchemaObj = departmentSchema.dump(data)
        return departmentSchemaObj'''

