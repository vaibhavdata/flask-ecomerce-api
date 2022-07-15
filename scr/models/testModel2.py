from scr.models import db
import enum
from scr.models import db, bcrypt
from scr.shred.MainService import Mainservice
from datetime import datetime
from marshmallow import Schema, fields, validates


class Userss(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'userss'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Test(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.userss.id', ondelete='SET NULL'), nullable=True)
    user = db.relationship('Userss', backref='public.test')

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Area(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('public.test.id', ondelete='SET NULL'), nullable=True)
    test = db.relationship('Test', backref='public.area', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.userss.id', ondelete='SET NULL'), nullable=True)
    user = db.relationship('Userss', backref='public.area', lazy=True)

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Issue(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'issue'
    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('public.area.id', ondelete='SET NULL'), nullable=True)
    area = db.relationship('Area', backref='public.issue', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.userss.id', ondelete='SET NULL'), nullable=True)
    user = db.relationship('Userss', backref='public.issue', lazy=True)

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
