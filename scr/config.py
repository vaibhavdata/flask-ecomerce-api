from dotenv import load_dotenv
import os

class Development(object):
    debug = True
    TESTING = False
    #secret_key = os.getenv('secret_key')
    SQLALCHEMY_DATABASE_URI= os.getenv("ecommerce_flask_database")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class Producation(object):
    debug = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("ecommerce_flask_database")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
config_file =dict(
    development =Development,
    production =Producation
)