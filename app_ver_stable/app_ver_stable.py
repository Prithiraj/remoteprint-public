from flask import Blueprint
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Api

from app_ver_stable.api.CloudPrintAPI import api as cloudprint
from app_ver_stable.api.DevicesAPI import api as devices
from app_ver_stable.api.HtmlAPI import api as htmlapi
from app_ver_stable.api.QueuesAPI import api as queues
from app_ver_stable.api.TriggerPrintAPI import api as triggerprint

blueprint = Blueprint('api_ver_stable', __name__, url_prefix='/api/stable')

api = Api(blueprint,
          title='Star Print', 
          version='stable',
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
