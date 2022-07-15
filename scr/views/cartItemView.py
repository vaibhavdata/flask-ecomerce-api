from scr.models.cartModel import Cart,CartSehema
from scr.models.cartItemModel import CartItem,CartItem_Schema
from flask import Flask, request, json, Response, Blueprint, g
from scr.models.serviceModel import Product
from scr.shred.authontication import Auth
from scr.shred.MainService import Mainservice,StatusType
from flasgger import swag_from
CartItem_api_view = Blueprint('cart Item view', __name__)
from scr.shred.MainService import Mainservice,StatusType


'''@CartItem_api_view.route('/add_cartItem/<product_id>',methods =["POST"])
@Auth.auth_required
def add_cartItem(current_user,product_id):
    data = request.get_json()
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    product =Product.getById(product_id)
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id,product_id =product.product_id).first()
    if cart_item:
        cart_item_get = CartItem.query.get_or_404(1)
        cart_item_get.quentive += 1
        cart_item_get.save()
    else:

        new_cart = CartItem(data)
        new_cart.save()


    cart_sehma = CartItem_Schema(only=['product_id','cart_item_id','cart_id','user_id','quentive'])
    result = cart_sehma.dumps(data)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "CartItem add successfully fetched"
    }
    return Mainservice.response(data=response, status_code=200)'''




@CartItem_api_view.route('/remove_cartItem/<product_id>/<cartItem_id>',methods =["GET"])
@Auth.auth_required
@swag_from("D://flask_ecommerce/scr/docs/cart/cart_item_delete.yml")
def remove_cartItem(current_user,product_id,cartItem_id):
    product = Product.query.filter_by(product_id=product_id).first()
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    cart_item = CartItem.query.filter_by(cart_id =cart.cart_id, product_id=product.product_id,cart_item_id=cartItem_id).first()
    cart_item.delete()
    response = {
        "status": StatusType.success.value,
        "data": None,
        "message": "CartItem  remove successfully"
    }
    return Mainservice.response(data=response, status_code=200)


@CartItem_api_view.route('/update_cart_item',methods =["POST"])

@Auth.auth_required
@swag_from("D://flask_ecommerce/scr/docs/cart/cart.yml")
def update_cart_item(current_user):
    data = request.get_json()
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    data.update({'cart_id': cart.cart_id})
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, product_id=data['product_id']).first()
    if cart_item:
        data['quentive'] += cart_item.quentive
        cart_item.update(data)
    else:
        new_cart_item = CartItem(data)
        new_cart_item.save()
    cart_sehma = CartItem_Schema()
    result = cart_sehma.dump(data)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "CartItem update and add  successfully"
    }
    return Mainservice.response(data=response, status_code=200)

