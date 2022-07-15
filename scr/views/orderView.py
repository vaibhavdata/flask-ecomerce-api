from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from scr.models.orderModel import Order,OrderSchema
from scr.shred.authontication import Auth
order_api = Blueprint('order view', __name__)
@order_api.route('/add_order',methods =["POST"])
@Auth.auth_required
def add_order(current_user):
    data = request.get_json()

    return "add order method"