from scr.models.categoryModel import Category,CategorySchema
from flask import Flask, request, json, Response, Blueprint, g
from scr.shred.MainService import Mainservice,StatusType
from scr.validations.categoryVali import CategoryValidation
from flask_restful import Api
from flasgger import swag_from
category_api = Blueprint('Category view', __name__,url_prefix="/api/")


@category_api.route('/category_data',methods=["GET"])
@swag_from("D://flask_ecommerce/scr/docs/category/category_get.yml")
def category_data():
    obj =Category.getAll()

    category_schema = CategorySchema(only=['category_id','name','is_delete','date_created','date_created'])

    category = category_schema.dumps(obj,many=True)
    response = {
        "status": StatusType.success.value,
        "data": category,
        "message": "Categories successfully fetched"
    }
    return Mainservice.response(data=response, status_code=200)





@category_api.route('/add_category',methods=['POST'])
@swag_from("D://flask_ecommerce/scr/docs/category/category_post.yml")
def add_category():
    data = request.get_json()
    category = Category(data)
    category.save()


    category_schema = CategorySchema(only=['name','is_delete','date_created','date_created'])

    result = category_schema.dump(category)

    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "category add succefully"
    }
    return Mainservice.response(data=response, status_code=200)

@category_api.route('/edit_category/<id>',methods =["POST"])
@swag_from("D://flask_ecommerce/scr/docs/category/category_update.yml")
def edit_category(id):
    data = request.get_json()
    category = Category.getById(data.get('category_id',''))
    print(category)
    if category:
        if category.category_id != int(id):
            response = {
                "status": StatusType.fail.value,
                "data": None,
                "message": "The category name provided already exists"
            }
            return Mainservice.response(data=response, status_code=200)
    categ = Category.getById(id)
    categ.update(data)
    category_schema = CategorySchema(only=['category_id', 'name', 'is_delete', 'date_created', 'updated_at'])

    result = category_schema.dump(categ)

    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "The category value updated succesfully"
    }
    return Mainservice.response(data=response, status_code=200)

@category_api.route('/delete_category/<id>',methods =["GET"])
@swag_from("D://flask_ecommerce/scr/docs/category/category_delete.yml")
def delete_category(id):
    category = Category.getById(id)
    if not category:
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": "category id not fount"
        }
        return Mainservice.response(data=response, status_code=200)




    category.delete(id)
    response = {
        "status": StatusType.success.value,
        "data": None,
        "message": "category delete succsefully"
    }
    return Mainservice.response(data=response, status_code=200)










