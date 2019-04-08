from flask import Flask, jsonify, request, make_response, g
from api.models.models import Incident, User,UserLogin
from . import views_blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from flask import current_app
from functools import wraps
from api.models.incident import IncidentController

from api import Create_app

app = Create_app('default')
 

dbconn = IncidentController()
# users_array =my_incident.users


@views_blueprint.route('/user/register', methods=['POST'])  
def registerUser():
    data= request.get_json()
    if request.method == 'POST':
        if not request.json or not 'firstname' in data or not 'lastname' in data or not 'email' in data\
         or not 'tel' in data or not 'password' in data:
            return jsonify({'message': 'bad request' , 'status': 404})

        registered_date = dbconn.date_generator() 
        hashed_password = generate_password_hash(data['password'], method='sha256', salt_length=8)
        IsAdmin= False  
        user = User(data['firstname'], data['lastname'],data['othernames'], \
        data['username'], hashed_password, data['email'], data['tel'], registered_date, IsAdmin) 
        registered_user=dbconn.add_user(user)
        if registered_user is False:
            return jsonify({'message':'user with this username or email already exists'}) 

        dbconn.sendmail(app.config['ADMIN_EMAIL'],'New user created', data['username'])
        return jsonify({'data': [{'id': registered_user.__dict__ ,'message': \
            'user has been registered'}], 'status': 201 })       
       
            # except ConnectionError as e:
            #     return jsonify({'msg': 'no internet connection'})
    return jsonify({'message': 'bad request' , 'status': 400})


@views_blueprint.route('/user/login', methods=['GET', 'POST'])  
def login():
    auth = request.authorization
    if not auth or not auth['username'] or not auth['password']:
        return make_response('could not verify you', 401,  {'www-authenticate':'Basic realm ="Login required!"'})
    a_user= UserLogin(auth.username, auth.password)
    user = dbconn.loginuser(a_user)
    if user is False:
         return make_response('could not verify you', 401,  {'www-authenticate':'Basic realm ="Login required!"'})
    else:
        token = jwt.encode({'id':user['user_id'], \
        'expiration': str(datetime.utcnow() + timedelta(seconds=3600)) }, current_app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})



