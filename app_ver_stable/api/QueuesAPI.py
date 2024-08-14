from distutils.log import error

from app_ver_stable.models.queues import Queue
from app_ver_stable.utilities.Trim import Trim
from flask import jsonify, request
from flask_restx import Namespace, Resource, abort, fields
from marshmallow import Schema, ValidationError
from marshmallow import fields as mmfields

api = Namespace('queues', description='queues related query')


list_queues = api.model('list_queues', {
    'id': fields.Integer(required=True, description='queue id'),
    'name': fields.String(required=True, description='queue name'),
    'position': fields.Integer(required=True, description='queue position')
})

saved_queue = api.model('queue_id', {
    'queue_id': fields.Integer(required=True, description='queue id')
})

row_count = api.model('row_count', {
    'row_count': fields.Integer(description='row count')
})

class QueueName(Schema):
    name = Trim(
        mmfields.String(), required=True, description='queue name',
                        error='please proivde a queue name'
    )

class QueueId(Schema):
    id = Trim(
        mmfields.Integer(), required=True, min=1, description='queue id',
                         error='please proivde a queue id'
    )

@api.route('/')
class QueuesAPI(Resource):
    
    @api.marshal_with(saved_queue)
    def post(self):
        try:
                
            payload = request.json
            data = QueueName().load(payload)
            name = data['name']
            print(name) 
            id = Queue.addQueue(name)
            return {
                'queue_id': id
            }
        except ValidationError as e:
            abort(402, e.args)
        except Exception as e:
            abort(502, e.args)
            
    @api.marshal_list_with(list_queues)
    def get(self):
        try:
            items = Queue.listQueues()
            data = []
            if items is not None:
                for item in items:
                    data.append({
                        "id": item.id,
                        "name": item.name,
                        "position": item.position
                    })
            return data
        except Exception as e:
            abort(502, e.args)
    
    @api.marshal_with(row_count)
    def delete(self):
        try:
            payload = request.json
            data = QueueId().load(payload)
            row_count = Queue.delQueue(data['id'])
            return {
                'row_count': row_count
            }
        except ValidationError as e:
            abort(402, e.args)
        except Exception as e:
            abort(502, e.args)
    
    @api.marshal_with(row_count)
    def put(self):
        try:
            payload = request.json
            data = QueueId().load(payload)
            queue_id = data['id']
            row_count = Queue.resetQueue(queue_id)
            return {
                'row_count': row_count
            }
        except ValidationError as e:
            abort(402, e.args)
        except Exception as e:
            abort(502, e.args)
