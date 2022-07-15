from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from scr.models.userpaymentmethod import UserpayMethod_schema,UserPayMethod
from scr.shred.authontication import Auth

user_payment_method = Blueprint("User payment method",__name__)
@user_payment_method.route('/add_userpay_method',methods=["POST"])
@Auth.auth_required
def add_userpay_method(current_user):
    data = request.get_json()
    user_paymethod = UserPayMethod(data)
    user_paymethod.save()
    userpay_schema = UserpayMethod_schema(only=['userPayMethod_id','user_id','payMethod_id','date_created','updated_at'])
    result = userpay_schema.dump(data)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "add user payment method  succsefully"
    }
    return Mainservice.response(data=response, status_code=200)


@user_payment_method.route('/userpay_method',methods=["GET"])
@Auth.auth_required
def userpay_method(current_user):
    user_pay_method = UserPayMethod.query.all()
    user_pay_schema = UserpayMethod_schema(many=True)
    result = user_pay_schema.dumps(user_pay_method)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "user payment method all type"
    }
    return Mainservice.response(data=response, status_code=200)
