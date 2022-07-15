from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from scr.models.plansModel import PlanModel,PlanSchema
from scr.shred.authontication import Auth

plan_on_product = Blueprint("plan provide by compny",__name__)
@plan_on_product.route('/add_plan/<product_id>',methods=["POST"])
@Auth.auth_required
def add_plan(current_user,product_id):
    data = request.get_json()
    plan_data = PlanModel(data)
    plan_data.save()
    plan_schema = PlanSchema(only =['name','price','is_type','is_active','date_created','updated_at','product_id'])
    result = plan_schema.dump(data)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "add plan  succsefully"
    }
    return Mainservice.response(data=response, status_code=200)

@plan_on_product.route('/plan/<product_id>/',methods=["GET"])
@Auth.auth_required
def plan(current_user,product_id):
    all_plan = PlanModel.query.all()
    plan_schema = PlanSchema(many=True)
    result = plan_schema.dumps(all_plan)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "all plans "
    }
    return Mainservice.response(data=response, status_code=200)