from scr.models.cartModel import Cart,CartSehema
from scr.models.cartItemModel import CartItem,CartItem_Schema
from flask import Flask, request, json, Response, Blueprint, g
from scr.models.serviceModel import Product
from scr.shred.authontication import Auth
from flasgger import swag_from
Cart_api_view = Blueprint('cart view', __name__)
from scr.shred.MainService import Mainservice,StatusType
@Cart_api_view.route('/cart',methods =["GET"])
@Auth.auth_required
def cart(current_user):
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id).first()
    cart_sehma = CartItem_Schema()
    result = cart_sehma.dumps(cart_item)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "cart items"
    }
    return Mainservice.response(data=response, status_code=200)



@Cart_api_view.route('/add_cart',methods =["POST"])
@Auth.auth_required
@swag_from("D://flask_ecommerce/scr/docs/cart/cart_add.yml")
def add_cart(current_user):
    data = request.get_json()

    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    cart_ = Cart(data)
    cart_.save()
    cart_schema = CartSehema()

    result = cart_schema.dump(cart)
    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "Cart  successfully fetched"
    }
    return Mainservice.response(data=response, status_code=200)

@Cart_api_view.route('/remove_cart/<product_id>/<cartItem_id>',methods =["GET"])
@Auth.auth_required
#@swag_from("D://flask_ecommerce/scr/docs/cart/cart_delete.yml")
def remove_cart(current_user,product_id,cartItem_id):
    product = Product.query.filter_by(product_id=product_id).first()
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, product_id=product.product_id,cart_item_id= cartItem_id).first()
    if cart_item.quentive > 1:
        cart_item.quentive -= 1
        cart_item.save()
    else:
        cart_item.delete()

    response = {
        "status": StatusType.success.value,
        "data": None,
        "message": "Cart quentity decress and remove  successfully"
    }
    return Mainservice.response(data=response, status_code=200)









