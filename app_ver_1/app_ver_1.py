from flask import Blueprint
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Api

from app_ver_1.api.CloudPrintAPI import api as cloudprint
from app_ver_1.api.DevicesAPI import api as devices
from app_ver_1.api.HtmlAPI import api as htmlapi
from app_ver_1.api.TriggerPrintAPI import api as triggerprint
from app_ver_1.api.QueuesAPI import api as queues

blueprint = Blueprint('api_ver_1', __name__, url_prefix='/api/1', template_folder='web/templates', static_folder='web/static')

api = Api(blueprint,
          title='Star Print', 
          version='1.0',
          description='API for Star Print'
          )

api.add_namespace(queues)
api.add_namespace(devices)
api.add_namespace(triggerprint)
api.add_namespace(cloudprint)
api.add_namespace(htmlapi)


@api.errorhandler(JWTExtendedException)
def handle_jwt_exceptions(error):
    return {'message': str(error)}, getattr(error, 'code', 401)
