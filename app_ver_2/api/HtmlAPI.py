from flask import render_template, Response, make_response
from flask_restx import Resource, Namespace

api = Namespace('web', description='return html')

@api.route('/')
class HtmlAPI(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('management.html'),200,headers)

@api.route('/print')
class HtmlPrintAPI(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('print.html'),200,headers)

@api.route('/doc')
class APIDoc(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('README.html'),200,headers)
