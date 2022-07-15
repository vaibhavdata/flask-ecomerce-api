import enum
import json
import datetime
import locale
import re
from datetime import timezone
import enum
from flask import Response

class Label(enum.Enum):
    sale= "Sale"
    new_item = "New_item"
    trending_now ="Trending_now"

class StatusType(enum.Enum):
    success = "SUCCESS"
    fail = "FAIL"
    error = "ERROR"

class Mainservice:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

    # Create response data
    @classmethod
    def responseModel(cls, values):
        if values.get('status') == StatusType.error.value:
            msg = cls.__setErrorMessages(values.get('data', ''))
            response = {
                "status": values.get('status', ''),
                "data": dict(),
                "message": msg,
                "errors": values.get('data', '')
            }
        else:
            try:
                data = json.loads(values.get('data', ''))
            except Exception as e:
                if type(values.get('data', '')) == dict:
                    data = values.get('data', '')
                else:
                    data = dict()
            response = {
                "status": values.get('status', ''),
                "data": data,
                "message": values.get('message', '')
            }
        response = json.dumps(response)
        return response

    # Response method
    @classmethod
    def response(cls, data, status_code):

        response = cls.responseModel(data)
        return Response(
            mimetype="application/json",
            response=response,
            status=status_code
        )

    # Error message create
    @staticmethod
    def __setErrorMessages(data):
        message = ""
        for k, v in data.items():
            if message:
                message = str(message) + str(', ') + str(v)
            else:
                message = str(v)
        return message

    @staticmethod
    def validation(fields,data):
        errors = {}
        for field in fields:
            name = field.replace('_', ' ')
            if data.get(field) is None or data.get(field) == "":
                errors[field] = f"The {name} field is required."
            else:
                if field == "email":
                    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                    if data.get(field) and not re.match(EMAIL_REGEX, data.get(field)):
                        errors[field] = f"The {name} field is not valid."
                if field == "product":
                    product = data.get(field)
                    for k, v in product.items():
                        if v is None or v == "":
                            n = k.replace('_', ' ')
                            errors[k] = f"The {n} field is required."
        return errors


    @staticmethod
    def UpdateDatetime():
        dateTime= datetime.datetime.now()
        return  dateTime
    @staticmethod
    def currentDatetime():
        dateTime = datetime.datetime.now(timezone.utc)
        return dateTime

