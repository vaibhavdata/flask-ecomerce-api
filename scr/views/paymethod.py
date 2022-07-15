from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from scr.models.paymentMethod import PayMethod,PayMethodSchema
from scr.shred.authontication import Auth
payment_method = Blueprint("payment method",__name__)
@payment_method.route('/add_pay_method',methods=["POST"])
@Auth.auth_required
def add_pay_method(current_user):
    data = request.get_json()
    pay_method = PayMethod(data)
    pay_method.save()
    pay_method_schema = PayMethodSchema(only=['name','date_created','updated_at','payMethod_id'])
    result = pay_method_schema.dump(data)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "add payment method  succsefully"
    }
    return Mainservice.response(data=response, status_code=200)

@payment_method.route('/pay_method',methods=["GET"])
@Auth.auth_required
def pay_method(current_user):
    all_method = PayMethod.query.all()
    pay_method_schema = PayMethodSchema(many=True)
    result = pay_method_schema.dumps(all_method)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "payment method all type"
    }
    return Mainservice.response(data=response, status_code=200)


