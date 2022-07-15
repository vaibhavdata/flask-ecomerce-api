from flask import Blueprint
from flask_restx import Api
from scr.views.role import UserApi as ns1
from scr.views.userView import user_detail as ns2



blueprint = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(blueprint,title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(ns1)
api.add_namespace(ns2)
