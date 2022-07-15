from scr.models.User import UserSchema,User,UserLoginSchema
from flask import Blueprint, request, jsonify, session
from scr.shred.MainService import Mainservice,StatusType
from scr.shred.authontication import Auth
from flasgger import swag_from

user_detail = Blueprint('User detaill ',__name__)

@user_detail.route('/register',methods =["POST"])
@swag_from('D://flask_ecommerce/scr/docs/user/user_register.yml')

def register():
    "user register"
    data = request.get_json()
    fields = ['email','first_name','last_name','username','mobile','is_staff','is_verified','role_id','password','confirm_password','is_active','is_admin']
    error = Mainservice.validation(fields, data)
    if error:
        response ={
            "status": StatusType.error.value,
            "data": error,
            "message": ""
        }
        return Mainservice.response(data=response,status_code=200)
    user = User.getByEmail(data.get('email',''))
    if user:
        response ={
            "status": StatusType.fail.value,
            "data": None,
            "message":"email allred exit"
        }
        return Mainservice.response(data=response,status_code=200)
    user_name = User.getByUsername(data.get('username',''))
    if user_name:
        response ={
            "status": StatusType.fail.value,
            "data": None,
            "message" :"user name allred exit"
        }
        return  Mainservice.response(data=response,status_code=200)

    if len(data.get('password','')) <6:
        respose ={
            "status": StatusType.fail.value,
            "data" : None,
            "message": "password is to short "
        }
        return Mainservice.response(data=respose,status_code=200)
    if data.get('password','') !=data.get('confirm_password',''):
        response ={
            "status": StatusType.fail.value,
            "data": None,
            "message": "Password and confirm_password not match"
        }
        return Mainservice.response(data= response,status_code=200)

    user = User(data)
    user.save()

    userSchema = UserSchema()
    user_data =userSchema.dump(user)
    response = {
        "status": StatusType.success.value,
        "data": user_data,
        "message": "user registerted succesfully"
    }
    return Mainservice.response(data= response,status_code=200)


@user_detail.route('/login',methods=["POST"])
@swag_from('D://flask_ecommerce/scr/docs/user/user_login.yml')
def login():
    "user login"
    data = request.get_json()
    fildes = ['email','password']
    error = Mainservice.validation(fildes,data)
    if error:
        response ={
            "status": StatusType.error.value,
            "data": error,
            "message": ""
        }
        return Mainservice.response(data=response,status_code=200)
    user = User.getByEmail(data.get('email'))
    if not user:
        response ={
            "status": StatusType.fail.value,
            "data": None,
            "message":" email not found here"
        }
        return Mainservice.response(data=response,status_code=200)
    if not user.check_hash(data.get('password')):
        response ={
            "status": StatusType.fail.value,
            "data":None,
            "message":"user password not hashing"
        }
        return Mainservice.response(data=response,status_code=200)

    userSchema = UserLoginSchema()
    user_data = userSchema.dump(user)
    token = Auth.generate_token(user_data.get('user_id', ''))
    response = {
        "status": StatusType.success.value,
        "data": {"token": str(token), "user": user_data},
        "message": "login succsefully"
    }
    return Mainservice.response(data=response, status_code=200)


@user_detail.route('/get_data',methods=["GET"])
def get_data():
    data = User.query.all()

    user_schema =UserSchema()

    result = user_schema.dumps(data,many=True)

    response = {
        "status": StatusType.success.value,
        "data": result,
        "message": "login succsefully"
    }
    return Mainservice.response(data=response, status_code=200)



