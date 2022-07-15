from flask import Flask
from flask import Blueprint
from scr.models import db,bcrypt
from scr.config import config_file
from scr.views.role import UserApi
from flask_migrate import Migrate
from scr.views.userView import user_detail
from scr.views.category import category_api
from scr.views.cart import Cart_api_view as cart_api
from scr.views.product import product_api
from scr.views.cartItemView import CartItem_api_view as cartitem_api
from scr.views.orderView import order_api
from scr.views.paymethod import payment_method
from scr.views.user_paymethod import user_payment_method
from scr.views.plans import plan_on_product
from scr.views.paymentview import payment_view
from scr.views.testView import testApi
#from flask_swagger_ui import UserApi
#from flask_restx import Api
#from flask_restplus import Api
from flasgger import Swagger,swag_from
from scr.shred.swaggerConfig import template,swagger_config
from flask_restful import Api

migrate = Migrate()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_file[config_name])
    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(UserApi,url_prefix='/api/')
    app.register_blueprint(user_detail, url_prefix='/api/')
    app.register_blueprint(category_api)
    app.register_blueprint(cart_api,url_prefix='/api/')
    app.register_blueprint(product_api,url_prefix='/api/')
    app.register_blueprint(cartitem_api, url_prefix='/api/')
    app.register_blueprint(order_api,url_prefix='/api/')
    app.register_blueprint(payment_method,url_prefix='/api/')
    app.register_blueprint(user_payment_method,url_prefix='/api/')
    app.register_blueprint(plan_on_product,url_prefix="/api/")
    app.register_blueprint(payment_view,url_prefix="/api/")
    app.register_blueprint(testApi,url_prefix='/api/')



    migrate.init_app(app,db)
    swagger = Swagger(app, config=swagger_config, template=template,parse=True)


    return app

