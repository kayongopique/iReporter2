
from flask import Flask, jsonify, request,current_app
from api.models.models import Incident
from . import views_blueprint
from api.models.incident import IncidentArray
from functools import wraps
my_incident = IncidentArray()
users_array =my_incident.users
# from api import Create_app


# app = Create_app('default')

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'msg': 'missing token'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'] )
            current_user={ user for user in users_array if user.id == data['id']}
        except:
            return jsonify({'msg': 'token has expired'})
        return func(current_user, *args, **kwargs)
    return decorated



@views_blueprint.route('/redflag/<int:id>/location', methods=['PATCH'])
@token_required
def edit_location(current_user, id):
        new_location = request.get_json()['location']
        redflag = my_incident.edit_location(id, new_location)
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404}) ,404
        else:
            if redflag[0]['status']!='draft':
                return jsonify({'data':[{'redflag':redflag, 'message': \
                'can not perform this operation because the record  is'\
                 +" "+ redflag[0]['status']}], 'status': 200})     
            return jsonify({'data':[{'id':id, 'message': \
            'Updated red-flag record location'}], 'status': 200})

@views_blueprint.route('/redflag/<int:id>/comment', methods=['PATCH'])
@token_required
def edit_comment(current_user, id):
        data = request.get_json()
        redflag = my_incident.edit_comment(id, data['comment'])
        if not redflag:
            return jsonify({'message': 'flag not found', 'status': 404}) ,404 
        else:
            if redflag[0]['status']!='draft':
                return jsonify({'data':[{'redflag':redflag, 'message': \
                'can not perform this operation because the record  is'\
                 +" "+ redflag[0]['status']}], 'status': 200})     
            return jsonify({'data':[{'id':id, 'message': \
            'Updated red-flag records comment '}], 'status': 200})

@views_blueprint.route('/redflag/<int:id>', methods=['PUT'])
@token_required
def edit_redflag(current_user, id):
        data = request.get_json()
        redflag = my_incident.edit_redflag(id, data['incidentType'], data['location'], data['comment'])
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404})
       
        return jsonify({'redflag': redflag[0]})
