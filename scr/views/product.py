from scr.models.serviceModel import Product,ProductSchema,PaginationSchema
from flask import Flask, request, json, Response, Blueprint, g
from flasgger import swag_from
from scr.shred.MainService import Mainservice,StatusType
from scr.models.categoryModel import Category
product_api = Blueprint('product view', __name__)

@product_api.route('/product',methods =["GET"])
#@swag_from("D://flask_ecommerce/scr/docs/product/product_get.yml")
def product():

    cate =Product.query.all()
    products_schema = ProductSchema()
    result = products_schema.dumps(cate,many=True)

    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "product detail"
    }
    return Mainservice.response(data=response, status_code=200)


@product_api.route('/product_list',methods =["GET"])
@swag_from("D://flask_ecommerce/scr/docs/product/product_serarch.yml")
def product_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per-page', 10))
    if request.args.get('product_name', '') or page or per_page:
        search = f"%{request.args.get('product_name', '')}%"
        product_query = Product.query.filter(Product.product_name.ilike(search)).order_by(Product.product_id.desc())
        product = product_query.paginate(page, per_page, error_out=False)
    else:
        product=Product.query.order_by(Product.product_id.desc()).paginate(page=page,per_page=per_page,error_out=True)

    page_schema = PaginationSchema()
    product_data = page_schema.dump(product.items,many=True)
    results = page_schema.dump(product)
    data = {
        "product_details":product_data,
        "page_info":results
    }



    response = {
        "status": StatusType.success.value,
        "data": data,
        "message": "product detail",
    }
    return Mainservice.response(data=response, status_code=200)




@product_api.route('/add_product',methods =["POST"])
@swag_from("D://flask_ecommerce/scr/docs/product/product_post.yml")
def add_product():
    data = request.get_json()

    product = Product(data)
    product.save()

    product_serlizer = ProductSchema()
    result = product_serlizer.dump(product)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "product  add succefully"
    }
    return Mainservice.response(data=response, status_code=200)

@product_api.route('/edit_product/<id>',methods =["POST"])
@swag_from("D://flask_ecommerce/scr/docs/product/product_update.yml")
def edit_product(id):
    data = request.get_json()
    product = Product.getById(data.get('product_id',''))
    if product:
        if product.product_id != int(id):
            response = {
                "status": StatusType.error.value,
                "data": None,
                "message": "product not exits here by id"
            }
            return Mainservice.response(data=response, status_code=200)
    prod = Product.getById(id)
    prod.update(data)
    product_serlizer = ProductSchema(
        only=['product_id', 'product_name', 'product_slug', 'is_delete', 'price', 'old_price', 'item_stock', 'is_plan',
              'date_created', 'updated_at', 'category_id'])
    result = product_serlizer.dump(prod)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "product update succsefully"
    }
    return Mainservice.response(data=response, status_code=200)

@product_api.route('/product_delete/<id>',methods =['GET'])
@swag_from("D://flask_ecommerce/scr/docs/product/product_delete.yml")
def product_delete(id):
    product = Product.getById(id)
    if not product:
        response = {
            "status": StatusType.fail.value,
            "data": None,
            "message": " id not found for here"
        }
        return Mainservice.response(data=response, status_code=200)
    else:


        product.delete()
        response = {
            "status": StatusType.success.value,
            "data": None,
            "message": "product  delete succsefully"
        }
        return Mainservice.response(data=response, status_code=200)
