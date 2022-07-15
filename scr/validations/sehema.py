from scr.models.testModel import Owners, Interests, OwnerInterests
from marshmallow import Schema, fields, validates


class InterestSchema(Schema):
    class Meta:
        fields = ('id', 'name')
        ordered = True


class OwnerInterestSchema(Schema):
    interest = fields.Nested(InterestSchema)

    class Meta:
        fields = ('id', 'interest', 'active')
        ordered = True


class OwnerSchema(Schema):
    owner = fields.Nested(OwnerInterestSchema, many=True)

    class Meta:
        fields = ('id', 'name', 'mobile', 'owner')
        ordered = True


'''''''#{"id": 1, "name": "ower1", "mobile": "1234", "owner": [{"id": 1, "active": true}, {"id": 2, "active": false}]}'''
