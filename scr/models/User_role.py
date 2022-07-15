from scr.models import db,ma
from sqlalchemy.sql import func
from scr.shred.MainService import Mainservice
from datetime import datetime,timezone
from marshmallow import Schema, fields, validates, ValidationError,validates_schema
class Role(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    #is_delete = db.Column(db.Boolean(), default=False,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default =Mainservice.currentDatetime(),nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True),default=Mainservice.UpdateDatetime(),onupdate=datetime.now(),nullable=False)

    def __repr__(self):
        return f'user role: {self.role_id}'
    def __init__(self,data):
        created_date = Mainservice.currentDatetime()
        update_at = Mainservice.UpdateDatetime()
        self.name = data.get('name','')
        self.date_created = created_date
        self.updated_at = update_at
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()






    @staticmethod
    def getAll():
        try:
            results = Role.query.all()
        except Exception as e:
            results = None
        finally:
            db.session.remove()
        return results

    @staticmethod
    def getById(Id):
        try:
            result = Role.query.filter_by(role_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

'''class RoleSchema(Schema):
    name = fields.String()
    is_delete = fields.Boolean(required=True)
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")'''
def validate_length(value):
    if len(value) <2:
        raise ValidationError('name must greter than 3.')
class RoleSchema(ma.SQLAlchemySchema):
    name = fields.Str(validate=validate_length)
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")
    is_delete =fields.Boolean()



    class Meta:
        fields =['role_id','name','date_created','updated_at','is_delete']
        model =Role



