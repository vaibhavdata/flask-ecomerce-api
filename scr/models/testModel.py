from scr.models import db
import enum
from sqlalchemy import Enum
from sqlalchemy.sql import func
from datetime import  datetime,timezone
from marshmallow import Schema, fields
class OwnerInterests(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'ownerinterests'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    owner_id = db.Column(db.Integer,db.ForeignKey('public.owners.id',ondelete='SET NULL'),nullable=True)
    interest_id = db.Column(db.Integer,db.ForeignKey('public.interests.id',ondelete='SET NULL'),nullable=True)
    active = db.Column(db.Boolean)


    def save(self):
        #self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Owners(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mobile = db.Column(db.String)
    owner = db.relationship('OwnerInterests', backref='public.owners', lazy=True)

    def save(self):
        #self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Interests(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    owner = db.relationship('OwnerInterests', backref='public.interests', lazy=True)

    def save(self):
        #self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()