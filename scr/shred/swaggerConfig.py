template = {
    "swagger": "2.0",
    "info": {
        "title": "Ecommerce API",
        "description": "API for Ecommerce",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "owebest@gmail.com",
            "url": "",
        },
        "termsOfService": "",
        "version": "1.0"
    },
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }

    },

}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'APISpecification',
            "route": '/APISpecification',
            "rule_filter": lambda rule: True,  # all in
            #"model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger_doc/",


}

