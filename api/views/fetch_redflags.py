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
            data = jwt.decode(token, current_app.config['SECRET_KEY'] )
            current_user={ user for user in users_array if user.id == data['id']}
        except:
            return jsonify({'msg': 'token has expired'})
        return func(current_user, *args, **kwargs)
    return decorated



@views_blueprint.route('/redflag', methods=['GET'])
@token_required
def all_redflags(current_user):
    redflags = my_incident.fetch_all_redflags()
    if not redflags:
        return jsonify({'message': ' no flags found', 'status' : 404}) ,404
    return jsonify({'data':redflags, 'status': 200})
 
@views_blueprint.route('/redflag/<int:id>', methods=['GET'])
@token_required
def specific_redflag(current_user, id):
    specific_flag = my_incident.fetch_specific_flag(id)
    if not specific_flag:
        return jsonify({'message': 'flag not found', 'status': 404}), 404
    return jsonify({'data': specific_flag, 'status': 200})

@views_blueprint.route('/user/<int:id>/redflags', methods=['GET'])
@token_required
def fetch_redflags_for_user(current_user, id):
    all_redflags_by_specificUser = [redflag for redflag in incidents_list if redflag['createdby']== id]
    return jsonify({'redfalgs': all_redflags_by_specificUser})

