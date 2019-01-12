from flask import Flask, jsonify, request
from api.models.models import Incident
from . import views_blueprint
from api.models.incident import IncidentArray
from functools import wraps
from flask import current_app

my_incident = IncidentArray()
users_array = my_incident.users


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
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = {user for user in users_array if user.id == data['id']}
        except:
            return jsonify({'msg': 'token has expired'})
        return func(current_user, *args, **kwargs)

    return decorated


@views_blueprint.route('/redflag', methods=['POST'])
@token_required
def create_redflag(current_user):
    data = request.get_json()
    if not request.json or not 'incidentType' in data or not 'location' in data or not 'comment' in data:
        return jsonify({'message': 'Some fields are empty, please cross check', 'status': 404}), 404
    status = my_incident.get_status()
    id = my_incident.incidentId_generator()
    owner = data['username']
    createdby = my_incident.createdby(owner)
    createdon = my_incident.date_generator()
    redflag = Incident(id, createdby, createdon, data['incidentType'], data['location'], status, data['comment'])
    my_incident.create_redflag(redflag)
    return jsonify({'data': [{'id': redflag.id, 'message': 'created redflag'}], 'status': 201}), 201