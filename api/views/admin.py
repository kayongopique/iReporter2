from flask import Flask, jsonify, request,current_app
from api.models.models import Incident
from . import views_blueprint
from api.models.incident import IncidentController
from functools import wraps
dbconn = IncidentController
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
            data = jwt.decode(token, app.config['SECRET_KEY'] )
            current_user={ user for user in users_array if user.id == data['id']}
        except:
            return jsonify({'msg': 'token has expired'})
        return func(current_user, *args, **kwargs)
    return decorated




@views_blueprint.route('/redflag/<int:id>/status', methods=['PATCH'])
@token_required
def update_status(current_user, id):
    if 'Isadmin' in current_user is False or not current_user:
        return jsonify({'msg': 'you dont have permission to perform this funtion'})
    new_status= request.get_json()['status']
    updated_status= dbconn.updateStatus('incidents',id , new_status)
    if not updated_status:
        return jsonify ({'message': 'flag not found', 'status': 404}), 404
    return jsonify({'data':[{'id': id , 'message': 'redflag status  has been updated to' +" "+ new_status}], \
    'status': 200 })



@views_blueprint.route('/users', methods=['GET'])
@token_required
def all_users(current_user):
    users = dbconn.fetch_all('users')
    if not users:
        return jsonify({'message': ' no flags found', 'status' : 404}) ,404
    return jsonify({'data':users, 'status': 200})

@views_blueprint.route('/user/<id>/admin', methods=['PUT'])
@token_required  
def promote_user(current_user, id):
    Admin = dbconn.promote_user(id)
    if Admin is None:
        return jsonify({'message': 'user not found!', 'status': 404})
    else:
        if Admin is True:
            return jsonify({'id':id, 'message': 'user has been promote to Admin'}) 


                 
                
 