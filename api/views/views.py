from flask import Flask,Blueprint, jsonify, request, make_response
from api.models.models import Incident, User, UserLogin
# from . import views_blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from flask import current_app
from functools import wraps
from api.models.incident import IncidentArray
 
# views_blueprint= Blueprint('views', __name__)
my_incident = IncidentArray()
users_array =my_incident.users
from api import Create_app


app = Create_app('default')

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
    redflag = Incident(id, createdby, createdon, data['incidentType'],data['location'],status, data['comment'])
    my_incident.create_redflag(redflag)
    return jsonify({'data': [{ 'id':redflag.id , 'message': 'created redflag'}], 'status': 201}) ,201

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

@views_blueprint.route('/redflag/<int:id>', methods=['DELETE'])
@token_required
def remove_redflag(current_user, id):
    flag= my_incident.delete_redflag(id)
    if not flag:
        return jsonify({'message': 'flag not found', 'status': 400}), 404 
    return jsonify({'data':[{'id': id , 'message': 'redflag has been deleted'}], 'status': 200})


@views_blueprint.route('/redflag/<int:id>/status', methods=['PATCH'])
@token_required
def update_status(current_user, id):
    if 'Isadmin' in current_user is False or not current_user:
        return jsonify({'msg': 'you dont have permission to perform this funtion'})
    new_status= request.get_json()['status']
    updated_status= my_incident.updateStatus(id , new_status)
    if not updated_status:
        return jsonify ({'message': 'flag not found', 'status': 404}), 404
    return jsonify({'data':[{'id': id , 'message': 'redflag status  has been updated to' +" "+ new_status}], \
    'status': 200 })


@views_blueprint.route('/user/register', methods=['POST'])  
def registerUser():
    data= request.get_json()
    if request.method == 'POST':
        if not request.json or not 'firstname' in data or not 'lastname' in data or not 'email' in data\
         or not 'tel' in data or not 'password' in data:
            return jsonify({'message': 'bad request' , 'status': 404})

        registered_date = my_incident.date_generator() 
        hashed_password = generate_password_hash(data['password'], method='sha256', salt_length=8)
        id = str(uuid.uuid4()) 
        IsAdmin= False  
        user = User(id, data['firstname'], data['lastname'],data['othernames'], \
        data['username'], hashed_password, data['email'], data['tel'], registered_date, IsAdmin) 
        my_incident.add_user(user)    
        return jsonify({'data': [{'id': user.id ,'message': 'user as been registered'}], 'status': 201 })  
    return jsonify({'message': 'bad request' , 'status': 400})


@views_blueprint.route('/user/<id>/admin', methods=['PUT'])
@token_required  
def promote_user(current_user, id):
    Admin = my_incident.promote_user(id)
    if Admin is None:
        return jsonify({'message': 'user not found!', 'status': 404})
    else:
        if Admin is True:
            return jsonify({'id':id, 'message': 'user has been promote to Admin'}) 


@views_blueprint.route('/users', methods=['GET'])
@token_required
def all_users(current_user):
    users = my_incident.fetch_all_users()
    if not users:
        return jsonify({'message': ' no flags found', 'status' : 404}) ,404
    return jsonify({'data':users, 'status': 200})
             


@views_blueprint.route('/user/login', methods=['GET', 'POST'])  
def login():
    auth = request.authorization
    if not auth or not auth['username'] or not auth['password']:
        return make_response('could not verify you', 401,  {'www-authenticate':'Basic realm ="Login required!"'})
    a_user= UserLogin(auth.username, auth.password)
    user = my_incident.loginuser(a_user)
    if user is False:
         return make_response('could not verify you', 401,  {'www-authenticate':'Basic realm ="Login required!"'})
    else:
        token = jwt.encode({'id':user[0].id, \
        'expiration': str(datetime.utcnow() + timedelta(seconds=3600)) }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})





    # data = request.get_json()
    # if request.method == 'POST':
    #     if 'username' in data and 'password' in data:
    #         a_user= UserLogin(data['username'], data['password'])
    #         person = my_incident.loginuser(a_user)
    #         if person:
    #             return jsonify({'message': 'youre logged in'})
    #         return jsonify({'message': 'please register first'})  
    #     return jsonify({'message': ' Some fields are missing' ,'status': 400})      
    # return jsonify({'message': 'login'})    

@views_blueprint.route('/user/<int:id>/redflags', methods=['GET'])
@token_required
def fetch_redflags_for_user(current_user, id):
    all_redflags_by_specificUser = [redflag for redflag in incidents_list if redflag['createdby']== id]
    return jsonify({'redfalgs': all_redflags_by_specificUser})



# if __name__== '__main__':
#     app.run(debug=False)


