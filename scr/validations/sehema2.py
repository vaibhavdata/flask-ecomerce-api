from scr.models.testModel2 import Userss,Test,Issue,Area
from scr.models import ma
class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Userss

class TestSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Test

class AreaSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Area

class IssueSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Issue






class Test_DetailedSchema(ma.SQLAlchemyAutoSchema):
    test = ma.Nested('TestSchema',many=True)
    user = ma.Nested('UserSchema',many=True)
    area = ma.Nested('AreaSchema',many=True)
    issue = ma.Nested('IssueSchema', many=True)