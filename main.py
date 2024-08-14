import os
from flask import Flask
from app_ver_1.app_ver_1 import blueprint as api_ver_1
from app_ver_2.app_ver_2 import blueprint as api_ver_2
from app_ver_stable.app_ver_stable import blueprint as api_ver_stable
from flask_cors import CORS

from flask_jwt_extended import JWTManager

import logging

logging.basicConfig(filename="logs/info.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__, static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
# app = Flask(__name__)


CORS(app, supports_credentials= True)

app.url_map.strict_slashes = False

app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = 'super-secret'

jwt = JWTManager()
jwt.init_app(app)

app.register_blueprint(api_ver_1, url_prefix='/api/1')
app.register_blueprint(api_ver_2, url_prefix='/api/2')
app.register_blueprint(api_ver_stable, url_prefix='/api/stable')

if __name__=='__main__':
    app.run('0.0.0.0', debug=True)