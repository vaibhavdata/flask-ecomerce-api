import json
import datetime
import locale
import re
from datetime import timezone
import enum
from flask import request
from scr.models.categoryModel import Category
from scr.shred.MainService import Mainservice,StatusType


class CategoryValidation:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')


    @classmethod
    def validation_name(cls,name,category_id=None):
        category = Category.query.filter(Category.name == name.lower().strip()).first()
        if category:
            if request.method =="PUT":
                if category_id != category.id:
                    response = {
                        "status": StatusType.fail.value,
                        "data": None,
                        "message": "The category name provided already exists"
                    }
                    return Mainservice.response(data=response, status_code=200)
            else:
                response = {
                    "status": StatusType.fail.value,
                    "data": None,
                    "message": "The category name provided already exists "
                }
                return Mainservice.response(data=response, status_code=200)

    @classmethod
    def validation(cls,data,category_id=None):
        name = data.get('name')
        if not name or not name.strip():
            response = {
                "status": StatusType.fail.value,
                "data": None,
                "message": "The category name not provide "
            }
            return Mainservice.response(data=response, status_code=200)





