import json
import os
import subprocess
import tempfile
from multiprocessing.sharedctypes import Value
from subprocess import PIPE, Popen

import requests
from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, abort, fields
from marshmallow import Schema, ValidationError
from marshmallow import fields as mmfields
from app_ver_stable.models.devices import Device
from app_ver_stable.models.queues import Queue
from app_ver_stable.utilities.convert import Convert
from app_ver_stable.utilities.PrintSupport import PrintSupport
from app_ver_stable.utilities.Trim import Trim
from app_ver_stable.utilities.validate import Validate

api = Namespace('cloudprint', description='webhook, cloud print related operations')

@api.route('/')
class CloudPrintAPI(Resource):

    def get(self):
        try:
            api.logger.info("PRINTING")
            content_type = request.args.get('type')
            devicemac = request.args.get('mac')
            
            basefile = tempfile.NamedTemporaryFile(prefix='markup')
            markupfile = basefile.name + ".stm"
            outputfile = tempfile.NamedTemporaryFile(prefix='output')
            
            printing, queue, width = Device.getDevicePrintRequired(devicemac)
            
            ticketDesign = Queue.getQueuePrintParameters(queue)
            api.logger.info("TICKET DESIGN \n" + str(ticketDesign.markup))
            
            PrintSupport.renderMarkupJob(markupfile, printing, queue, ticketDesign)
            PrintSupport.getCPConvertedJob(markupfile, content_type, width, outputfile, ticketDesign)

            
            outputfile.seek(0)
            output_content = outputfile.read()
            # api.logger.info("OUTPUT FILE INFO " + str(output_content))
            
            basefile.close()
            # markupfile.close()
            outputfile.close()
            # output_content = '0@18'
            
            response = Response(output_content, status=200)
            response.headers["Content-Type"] = content_type
            # response.headers["Content-Length"] = len(output_content)
            
            return response
        except Exception as e:
            abort(502, e.args)

    def post(self):
        try:
            payload = request.json
            # api.logger.info(payload)
            pollResponse = { }
            pollResponse['jobReady'] = False
            
            devicemac = payload['printerMAC']
            status = requests.utils.unquote(payload['statusCode'])
            isDeviceRegistered = Device.setDeviceStatus(devicemac, status)
            # api.logger.info("IS DEVICE REGISTERED : "+ str(isDeviceRegistered))
            clientActions = payload['clientAction']
            
            if not bool(isDeviceRegistered):
                pass
            elif bool(clientActions):
                width = 0
                ctype = "" 
                cver = "" 
                
                for i in range(len(clientActions)):
                    if clientActions[i]['request']=='PageInfo':
                        width = int(clientActions[i]['result']['printWidth']) * int(clientActions[i]['result']['horizontalResolution'])
                    elif clientActions[i]['request']=='ClientType':
                        ctype = str(clientActions[i]['result'])
                    elif clientActions[i]['request']=='ClientVersion':
                        cver = str(clientActions[i]['result'])
                
                Device.setDeviceInfo(devicemac, width, ctype, cver)
                
            else:
                item = Device.getDeviceOutputWidth(devicemac)
                printWidth = Convert.toInt(item.dot_width)
                if int(printWidth) == 0:
                    pollResponse['clientAction'] = [] 
                    pollResponse['clientAction'].append({"request": "PageInfo", "options": ""})
                    pollResponse['clientAction'].append({"request": "ClientType", "options": ""})
                    pollResponse['clientAction'].append({"request": "ClientVersion", "options": ""})

                else:
                    printing, queue, dotwidth = Device.getDevicePrintRequired(devicemac)
                      
                    isQueue = bool(queue)
                    isPrintEmpty = Validate.isEmpty(printing) 
                    isPrinting = Validate.isSet(printing)
                    
                    if (isQueue and not isPrintEmpty and isPrinting):
                        pollResponse['jobReady'] = True
                        item = PrintSupport.getCPSupportedOutput("text/vnd.star.markup") 
                        pollResponse['mediaTypes'] = item  # ["application/vnd.star.line","application/vnd.star.linematrix","application/vnd.star.starprnt","application/vnd.star.starprntcore","text/vnd.star.markup"] # PrintSupport.getCPSupportedOutput("text/vnd.star.markup")
            
            return jsonify(pollResponse) 
        except Exception as e:
            abort(502, e.args)
    
    def put(self):
        try:
            pass
        except Exception as e:
            abort(502, e.args)
    
    def delete(self):
        try:
            clearJobFromDB = True
            status = request.args.get('code')
            devicemac = request.args.get('mac')
            headerCode = status[0:1]
            
            if headerCode != "2":
                fullCode = status[0:3]
                if fullCode == "520":
                    clearJobFromDB = False
            
            if clearJobFromDB:
                Device.setCompleteJob(devicemac)
        
        except Exception as e:
            abort(502, e.args)
