from flask import Flask, jsonify, request, make_response
from api.models.models import Incident, User, UserLogin
from . import views_blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from flask import current_app
from functools import wraps
from api.models.incident import IncidentArray
 

my_incident = IncidentArray()
users_array =my_incident.users

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



