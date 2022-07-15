from scr.models.testModel import Owners,Interests,OwnerInterests
from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from scr.validations.sehema import OwnerSchema,InterestSchema,OwnerInterestSchema
from scr.validations.sehema2 import UserSchema,TestSchema,AreaSchema,IssueSchema,Test_DetailedSchema
testApi = Blueprint('test view', __name__)
@testApi.route('/test',methods =["POST"])
def test_add():
    data = request.get_json()
    owner = Owners(data)
    owner.save()

    response = {
        "status": StatusType.success.value,
        "data": data,
        "message": "The role define  succesfully"
    }
    return Mainservice.response(data=response, status_code=200)