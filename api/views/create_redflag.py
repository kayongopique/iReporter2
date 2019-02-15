from flask import Flask, jsonify, request,g
from api.models.models import Incident, StudentGrade
from . import views_blueprint
from api.models.incident import IncidentController
from functools import wraps
import jwt
from flask import current_app

dbconn = IncidentController()



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
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = dbconn.fetch_specific_user('users',data['id'])
        except:
            return jsonify({'msg': 'token has expired'})
        return func(current_user, *args, **kwargs)

    return decorated
@views_blueprint.route('/grades', methods=['POST'])
def create_grade():
    data = request.get_json()  
    grades = StudentGrade(data['studentno'],data['maths'],data['eng'],data['lug'],data['chem'])
    return jsonify({'message':'grade captured','grades':grades.__dict__})  


@views_blueprint.route('/redflag', methods=['POST'])
@token_required
def create_redflag(current_user):
    data = request.get_json()
    if not request.json or not 'incidentType' in data or not 'location' in data or not 'comment' in data:
        return jsonify({'message': 'Some fields are empty, please cross check', 'status': 404}), 404
    status = dbconn.get_status()
    createdby = current_user['user_id']
    createdon = dbconn.date_generator()
    redflag = Incident(createdby, createdon, data['incidentType'], \
    data['location'], status, data['comment'])
    dbconn.create_redflag(redflag)
    return jsonify({'data': [{'id': redflag.__dict__, 'message': 'created redflag'}], 'status': 201}), 201