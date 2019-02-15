from flask import Flask, jsonify, request,current_app
from api.models.models import Incident
from . import views_blueprint
from api.models.incident import IncidentController
from functools import wraps
import jwt 
dbconn = IncidentController()
# users_array =my_incident.users
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
        
        data = jwt.decode(token, current_app.config['SECRET_KEY'] )
        current_user =dbconn.fetch_specific_user('users',data['id'])
        
            # return jsonify({'msg': 'token has expired'})
        return func(current_user, *args, **kwargs)
    return decorated


@views_blueprint.route('/redflag', methods=['GET'])
@token_required
def all_redflags(current_user): 
    redflags = dbconn.fetch_all('incidents')
    if not redflags:
        return jsonify({'message': ' no flags found', 'status' : 404}) ,404
    return jsonify({'data':redflags, 'status': 200})
 
@views_blueprint.route('/redflag/<int:id>', methods=['GET'])
# @token_required
def specific_redflag( id):
    specific_flag = dbconn.fetch_specific_flag('incidents',id)
    if not specific_flag:
        return jsonify({'message': 'flag not found', 'status': 404}), 404
    return jsonify({'redflag': specific_flag, 'status': 200})

@views_blueprint.route('/user/redflags/<int:id>', methods=['GET'])
@token_required
def fetch_redflags_for_user(current_user, id):
    all_redflags_by_specificUser = dbconn.fetch_all_for_user('createdby',id)
    return jsonify({'redfalgs': all_redflags_by_specificUser})

