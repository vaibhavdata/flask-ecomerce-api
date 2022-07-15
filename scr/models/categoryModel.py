from scr.models import db,ma
from scr.shred.MainService import Mainservice
from marshmallow import Schema, fields,validate,ValidationError
import datetime
class Category(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'category'

    category_id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100),unique=True, nullable=False)
    is_delete = db.Column(db.Boolean,default=False,nullable=False)

    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.datetime.utcnow(), nullable=False)

    def __repr__(self):
        return f'category : {self.category_id}'


    def __init__(self,data):
        self.name = data.get('name','')
        self.is_delete=data.get('is_delete','')
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

    def delete(self,id):
        category = Category.query.filter_by(category_id=id).first()
        category.is_delete=True
        db.session.commit()

    @staticmethod
    def getById(Id):
        try:
            result = Category.query.filter_by(category_id=Id,is_delete="True").first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getAll():
        try:
            results = Category.query.all()
        except Exception as e:
            results = None
        finally:
            db.session.remove()
        return results

    @staticmethod
    def get_is_delete(id):
        try:
            result = Category.query.filter_by(category_id=id,is_delete ="True")
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result






class CategorySchema(ma.SQLAlchemySchema):
    category_id = fields.Int()
    name = fields.Str()
    is_delete = fields.Boolean()
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")

    '''class Meta:
        fields =('category_id','name','date_created','updated_at','is_delete')
        model = Category'''


