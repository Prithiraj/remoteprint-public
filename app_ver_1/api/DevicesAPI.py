# from ast import Try
# from distutils.log import error
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, abort
from app_ver_1.models.devices import Device
from marshmallow import Schema, fields as mmfields, ValidationError

from app_ver_1.utilities.Trim import Trim


api = Namespace('devices', description='devices related query')


list_devices = api.model('list_devices', {
	'devicemac': fields.String(required=True, description='device mac address'),
	'status': fields.String(required=True, description='connection status of the device'),
	'queue_id': fields.String(required=True, description='associated queue id'),
	'queue_name': fields.String(description='queue name'),
	'client_type': fields.String(description='client type'),
	'client_version': fields.String(description='client version'),
	'last_poll': fields.String(description='last poll'),
    'tray_status': fields.String(description='Tray status either working or not working')
})


devicemac = api.model('devicemac_queue_id', {
	'devicemac': fields.String(required=True, description='device mac address')
})

row_count = api.model('row_count', {
    'row_count': fields.Integer(description='row count')
})

class DeviceEntry(Schema):
    devicemac = Trim(mmfields.String(),required=True, description='device mac address')
    queueId = Trim(mmfields.Integer(), required=True, description='queue id')
    
class DeviceMac(Schema):
    devicemac = Trim(mmfields.String(), required=True, description='device mac address')
    
@api.route('/')
class DevicesAPI(Resource):
    @api.marshal_with(devicemac)
    def post(self):
        try:
            payload = request.json
            data = DeviceEntry().load(payload)
            print(data)
            devicemac = data['devicemac']
            queue_id = data['queueId']
            
            mac_id = Device.addDevice(devicemac, queue_id)
            
            return {
				'devicemac': mac_id
			}
        
        except ValidationError as e:
            abort(402, e.args)
            
        except Exception as e:
            abort(502, e.args)
    
    @api.marshal_list_with(list_devices)
    def get(self):
        try:
            items = Device.listDevices()
            data = []
            if items is not None:
                for item in items:
                    data.append({
                        "devicemac": item.devicemac,
                        "status": item.status,
                        "queue_id": item.queue_id,
                        "queue_name": item.queue_name,
                        "client_type": item.client_type,
                        "client_version": item.client_version,
                        "last_poll": item.last_poll
                    })
            return data
        except Exception as e:
            abort(502, e.args)
    
    def put(self):
        pass
    
    def delete(self):
        try:
            payload = request.json
            data = DeviceMac().load(payload)
            devicemac = data['devicemac']
            row_count = Device.delDevice(devicemac)
            row_count = {
				'row_count': row_count
			}
            return row_count
        except Exception as e:
            abort(402, e.args)
            