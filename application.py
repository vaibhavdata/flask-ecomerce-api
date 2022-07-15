from scr.app import create_app
from dotenv import load_dotenv,find_dotenv

import os
load_dotenv(find_dotenv())
env_name = os.getenv('FLASK_ENV')
application =create_app(env_name)


if __name__=="__main__":
    port = os.getenv('FLASK_PORT')
    application.run(host='0.0.0.0', port=port)