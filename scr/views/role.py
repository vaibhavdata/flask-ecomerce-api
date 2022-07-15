from scr.models.User_role import Role,RoleSchema
from scr.models.User import User,UserSchema
from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from flask_restx import Api,Namespace
from flasgger import swag_from
UserApi = Blueprint('user view', __name__)

@UserApi.route('/user_role',methods =["POST"])
@swag_from('D://flask_ecommerce/scr/docs/user_role/role.yml')
def user_role():
    data = request.get_json()
    fields = ['name','date_created','updated_at']


    user_role = Role(data)
    user_role.save()

    user_role_schema = RoleSchema(only=['name','role_id','date_created','updated_at'])
    data= user_role_schema.dump(data)
    response = {
        "status": StatusType.success.value,
        "data": data,
        "message": "The role define  succesfully"
    }
    return Mainservice.response(data=response, status_code=200)
@UserApi.route('/edit_role/<id>',methods=["POST"])
@swag_from('D://flask_ecommerce/scr/docs/user_role/role_update.yml')
def edit_role(id):
    data = request.get_json()
    user_data = Role.getById(id)
    user_data.update(data)

    user_role_schema = RoleSchema(only=('name','date_created', 'updated_at'))
    data = user_role_schema.dump(user_data)
    response = {
        "status": StatusType.success.value,
        "data": data,
        "message": "The role value updated succesfully"
    }
    return Mainservice.response(data=response, status_code=200)



@UserApi.route('/user_data',methods=["GET"])
@swag_from('D://flask_ecommerce/scr/docs/user_role/role_get.yml')
def user_data():
    data = Role.query.first()
    user_schema = RoleSchema()
    data = user_schema.dump(data)
    response = {
        "status": StatusType.success.value,
        "data": data,
        "message": "The role value updated succesfully"
    }
    return Mainservice.response(data=response, status_code=200)

@UserApi.route('/delete_role/<id>',methods=["GET"])
@swag_from('D://flask_ecommerce/scr/docs/user_role/role_delete.yml')
def delete_role(id):
    role = Role.getById(id)

    if not role:
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": "role id not found"
        }
        return Mainservice.response(data=response, status_code=200)
    role.delete()
    response = {
        "status": StatusType.success.value,
        "data": None,
        "message": "role user delete succsefully"
    }
    return Mainservice.response(data=response, status_code=200)


