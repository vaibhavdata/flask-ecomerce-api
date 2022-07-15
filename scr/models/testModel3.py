from scr.models import db


class Customer(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(100))
    password = db.Column(db.String(30))

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Gallery(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('public.customer.id', ondelete='SET NULL'), nullable=True)
    # uploads = db.relationship('Upload', backref='public.gallery')
    customer = db.relationship('Customer', backref='public.gallery')

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Upload(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    state = db.Column(db.String(20))
    gallery_id = db.Column(db.Integer, db.ForeignKey('public.gallery.id', ondelete='SET NULL'), nullable=True)
    gallery = db.relationship('Gallery', backref='public.upload')

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Location(db.Model):
    __table_args__ = ({"schema": "public"})
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    type = db.Column(db.String)
    upload_id = db.Column(db.Integer, db.ForeignKey('public.upload.id', ondelete='SET NULL'), nullable=True)
    upload = db.relationship('Upload', backref='public.location')

    def save(self):
        # self.date_created = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
