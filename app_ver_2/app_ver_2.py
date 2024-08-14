from flask import Blueprint
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Api

from app_ver_2.api.CloudLabelPrintAPI import api as cloudlabelprint
from app_ver_2.api.CloudPrintAPI import api as cloudprint
from app_ver_2.api.DevicesAPI import api as devices
from app_ver_2.api.HtmlAPI import api as htmlapi
from app_ver_2.api.TriggerPrintAPI import api as triggerprint
from app_ver_2.api.QueuesAPI import api as queues
from app_ver_2.api.TriggerLabelPrintAPI import api as triggerlabelprint

blueprint = Blueprint('api_ver_2', __name__, url_prefix='/api/2', template_folder='web/templates', static_folder='web/static') 

api = Api(blueprint,
          title='Star Print', 
          version='1.1',
          description='API for Star Print'
          )

api.add_namespace(queues)
api.add_namespace(devices)
api.add_namespace(triggerprint)
api.add_namespace(cloudprint)
api.add_namespace(cloudlabelprint)
api.add_namespace(htmlapi)
api.add_namespace(triggerlabelprint)


@api.errorhandler(JWTExtendedException)
def handle_jwt_exceptions(error):
    return {'message': str(error)}, getattr(error, 'code', 401)
