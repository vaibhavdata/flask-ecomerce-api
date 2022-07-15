from flask_marshmallow import Schema, fields
from scr.models.testModel3 import Customer, Location, Upload, Gallery


class LocationSchema(Schema):
    class Meta:
        fields = ('lat', 'long', 'type', 'upload_id')
        ordered = True


class UploadsSchema(Schema):
    location = fields.Nested(LocationSchema)

    class Meta:
        fields = ('id', 'state', 'location', 'gallery_id')
        ordered = True


class GallerySchema(Schema):
    uploads = fields.Nested(UploadsSchema, many=True)

    class Meta:
        fields = ('id', 'uploads')
        ordered = True
