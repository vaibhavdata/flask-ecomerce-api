import jwt
import os
import datetime
from flask import request, g
from functools import wraps
from scr.shred.MainService import Mainservice,StatusType
from scr.models.User import UserSchema,User

class Auth:
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                'iat': datetime.datetime.utcnow(),
                'user_id': user_id
            }
            token = jwt.encode(
                payload=payload,
                key=os.getenv('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
            try:
                if "b'" in str(token):
                    token = token.decode('utf-8')
            except Exception as e:
                print(f"Token generating error ==> {e}")
                pass
            return token
        except Exception as e:
            print(f"Token error ==> {e}")
            response = {
                "status": StatusType.fail.value,
                "data": None,
                "message": f"Error in generating user token: {str(e)}"
            }
            return Mainservice.response(data=response, status_code=403)

    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """

        @wraps(func)
        def decorated_auth(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
                token = token.split(' ')[1]
            # return 401 if token is not passed
            if not token:
                response = {
                    "status": StatusType.fail.value,
                    "data": None,
                    "message": "Token is missing!"
                }
                return Mainservice.response(data=response, status_code=401)
            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(
                    jwt=token,
                    key=os.getenv('JWT_SECRET_KEY'),
                    algorithms=["HS256"],
                )
                current_user = User.getById(data.get('user_id', ''))
            except jwt.ExpiredSignatureError:
                response = {
                    "status": StatusType.fail.value,
                    "data": None,
                    "message": "Token expired, please login again!"
                }
                return Mainservice.response(data=response, status_code=401)
            except jwt.InvalidTokenError:
                response = {
                    "status": StatusType.fail.value,
                    "data": None,
                    "message": "Invalid token, please try again with a new token!"
                }
                return Mainservice.response(data=response, status_code=401)
            return func(current_user, *args, **kwargs)

        return decorated_auth
