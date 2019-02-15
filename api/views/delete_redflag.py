from flask import Flask, jsonify, request, current_app
from api.models.models import Incident
from . import views_blueprint
from api.models.incident import IncidentController
from functools import wraps
dbconn= IncidentController()
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
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'] )
            current_user={ user for user in users_array if user.id == data['id']}
        except:
            return jsonify({'msg': 'token has expired'})
        return func(current_user, *args, **kwargs)
    return decorated
 

@views_blueprint.route('/redflag/<int:id>', methods=['DELETE'])
# @token_required
def remove_redflag( id):
    flag= dbconn.delete_redflag('incidents',id)
    if not flag:
        return jsonify({'message': 'flag not found', 'status': 400}), 404 
    return jsonify({'data':[{'id': id , 'message': 'redflag has been deleted'}], 'status': 200})

