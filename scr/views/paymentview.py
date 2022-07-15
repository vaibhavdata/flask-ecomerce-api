from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from scr.models.paymentModel import Payment,PaymentSchema
from scr.shred.authontication import Auth

payment_view = Blueprint("payment view",__name__)
@payment_view.route('/add_payment',methods =["POST"])
@Auth.auth_required
def add_payment(current_user):
    data = request.get_json()
    payment = Payment(data)
    payment.save()
    payment_serlize = PaymentSchema(only=["amount","date_created","updated_at","plan_id","product_id","user_id","userPayMethod_id","is_payment"])
    result = payment_serlize.dump(data)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "add payment method  succsefully"
    }
    return Mainservice.response(data=response, status_code=200)




@payment_view.route('/payment',methods =["GET"])
@Auth.auth_required
def payment(current_user):
    data = Payment.query.all()
    payment_serlize = PaymentSchema(many=True)
    result = payment_serlize.dumps(data)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "payment value "
    }
    return Mainservice.response(data=response, status_code=200)