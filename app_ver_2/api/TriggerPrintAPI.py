from multiprocessing.sharedctypes import Value

from flask import jsonify, request
from flask_restx import Namespace, Resource, abort, fields
from marshmallow import Schema, ValidationError
from marshmallow import fields as mmfields
from app_ver_2.models.devices import Device
from app_ver_2.models.queues import Queue
from app_ver_2.starmarkupengine.schema_validators.BuzzerCountSchema import \
    BuzzerCountSchema
from app_ver_2.starmarkupengine.schema_validators.DrawerSchema import DrawerSchema
from app_ver_2.starmarkupengine.StarMarkupEngine import StarMarkupEngine
from app_ver_2.starmarkupengine.tags import DrawerOpenModes
from app_ver_2.starmarkupengine.value_validators.ValueValidators import must_not_be_blank
from app_ver_2.utilities.Trim import Trim

api = Namespace('print', description='print related query')

generic_message = api.model('generic_message', {
    'message': fields.String(description='generic message'),
    'position': fields.String(description='Position')
})

class PrintInput(Schema):
    devicemac = Trim(mmfields.String(), required=True, description='device mac address')
    print_json = mmfields.List(mmfields.Dict, description='to be printed')
    drawer = mmfields.Dict(keys=mmfields.Str()) 
    buzzerCount = mmfields.Dict(keys=mmfields.Str(), validate = must_not_be_blank)

@api.route('/')
class TriggerPrint(Resource):

    @api.marshal_with(generic_message)
    def post(self):
        try:
            payload = request.json
            data = PrintInput().load(payload)
            api.logger.info(data)
            devicemac = data['devicemac']
            print_json = data['print_json']
            drawer = data['drawer'] if 'drawer' in data else None
            buzzer_count = data['buzzerCount'] if 'buzzerCount' in data else None
            
            drawer_open_at = DrawerOpenModes.NONE.name
            if bool(drawer) is True:

                drawer_data = DrawerSchema().load(drawer)
                drawer_open_at = drawer_data['openAt']
            
            if bool(buzzer_count) is True:

                buzzer_data = BuzzerCountSchema().load(buzzer_count)
                
                buzzer_start = buzzer_data['start'] if 'start' in buzzer_data else 0
                buzzer_end = buzzer_data['end'] if 'end' in buzzer_data else 0
                
            data = Device.getQueueIDandPrintingState(devicemac)
            
            printing = data.printing
            queue_id = data.queue_id
            width = data.dot_width
           
            markup = StarMarkupEngine.convertBillsToStarMarkup(print_json, width)
 
            if bool(queue_id) == False:
                abort(402, 'Non-existing queue_id')
            
            if printing is not None and printing > 0:
                return
            
            position = Queue.getPosition(queue_id)
            if bool(position) == False:
                abort(402, 'position isn\'t set')
                
            row_count = Queue.updatePosition(queue_id, markup, drawer_open_at, buzzer_start, buzzer_end)
            if bool(row_count) == False:
                abort(402, 'row isn\'t affected')
            
            row_count = Device.setDevicePrinting(devicemac, position)
            if bool(row_count) == False:
                abort(402, 'row isn\'t affected')
            
            api.logger.info("POSITION : " + str(position))
            return {
                'position': position
            }
             
        except ValueError as e:
            abort(402, e.args)
            
        except Exception as e:
            abort(502, e.args)
