import flask_bcrypt
import enum

import scr.models.User_role
from scr.models import db,bcrypt,ma
from scr.shred.MainService import Mainservice
from datetime import  datetime
from marshmallow import Schema, fields, validates
from werkzeug.security import generate_password_hash,check_password_hash
from scr.models.User_role import Role,RoleSchema

class UserType(enum.Enum):
    user = "User"
    admin ="Admin"

class User(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(250), nullable=True)
    last_name = db.Column(db.String(250), nullable=True)
    username  = db.Column(db.String(250), nullable=False,unique=True)
    email = db.Column(db.String(250), nullable=False,unique=True)
    mobile = db.Column(db.Integer, nullable=False,unique=True)
    is_admin  = db.Column(db.Boolean(), default=False,nullable=False)
    is_staff = db.Column(db.Boolean(), default=False,nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean(), default=False,nullable=False)
    role = db.relationship('Role', backref='public.user')
    role_id = db.Column(db.Integer,db.ForeignKey('public.role.role_id',ondelete='SET NULL'),nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=Mainservice.currentDatetime(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=Mainservice.UpdateDatetime(), onupdate=datetime.now(), nullable=False)

    def __repr__(self):
        return f'batch: {self.user_id}'
    def __init__(self,data):
        #self.user_id = data.get('user_id')
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.mobile = data.get('mobile', '')
        self.username = data.get('username', '')
        self.email = data.get('email', '')
        #self.password = data.get('password', '')
        self.password = self.__generate_password_hash(data.get('password', ''))
        self.date_created = Mainservice.currentDatetime()
        self.updated_at = Mainservice.UpdateDatetime()
        self.role_id = data.get('role_id', '')
        self.is_active = data.get('is_active',False)
        self.is_verified = data.get('is_verified','')
        self.is_staff  = data.get('is_staff','')
        self.is_admin =data.get('is_admin',False)

    def update(self, data):
        for key, item in data.items():
            if key =="password":
                self.password = self.__generate_password_hash(data.get('password',''))
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

    def __generate_password_hash(self,password):
        if password is not  None and password !='':
            return bcrypt.generate_password_hash(password,rounds=10).decode('utf-8')
        else:
            return ""

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    def __is_admin(self,admin):
        if self.is_admin==True:
            return UserType.admin.value
        elif 'Admin' in [r.name for r in self.role_id]:
            return UserType.admin.value
        else:
             return UserType.user.value



    @staticmethod
    def getById(Id):
        try:
            result = User.query.filter_by(user_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result
    @staticmethod
    def getByUsername(username):
        try:
            result = User.quert.filter_by(username=username).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    @staticmethod
    def getByEmail(email):
        try:
            result = User.query.filter_by(email=email,is_active=True).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result
    @staticmethod
    def getByRoleId(Id):
        try:
            result = User.query.filter_by(role_id=Id).first()
        except Exception as e:
            result = None
        finally:
            db.session.remove()
        return result

    #def is_admin(self):
        #return self.type == UserType.admin.name
class UserSchema(Schema):
    user_id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email  = fields.Str()
    password = fields.Str()
    mobile = fields.Int()
    is_admin = fields.Boolean()
    is_active = fields.Boolean(required=True)
    is_staff = fields.Boolean()
    date_created = fields.DateTime("%d/%m/%Y")
    updated_at = fields.DateTime("%d/%m/%Y")
    role_id  = fields.Int()
    is_verified = fields.Boolean()
    username = fields.Str()
    role = fields.Nested(RoleSchema)

'''class UserSchema(Schema):
    role = fields.Nested(RoleSchema)
    #role = fields.Pluck(RoleSchema, 'name')
    class Meta:
        fields =("user_id","first_name","last_name","role","password","email")
        model = User'''

class UserLoginSchema(Schema):
    class Meta:
        fields =("user_id","email","password")






