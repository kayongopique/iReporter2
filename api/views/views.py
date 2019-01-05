from flask import Flask, jsonify, request
from datetime import datetime
from api import app
from api.models.models import Incident, User, UserLogin

from api.models.incident import IncidentArray
 

my_incident = IncidentArray()


@app.route('/api/v1/redflag', methods=['POST'])
def create_redflag():
    data = request.get_json() 
    if not request.json or not 'incidentType' in data or not 'location' in data or not 'comment' in data:
        return jsonify({'message': 'Some fields are empty, please cross check', 'status': 404}), 404
    status = my_incident.get_status() 
    id = my_incident.incidentId_generator()
    owner = data['username']
    createdby = my_incident.createdby(owner)
    createdon = my_incident.incidentDate_generator()
    redflag = Incident(id, createdby, createdon, data['incidentType'],data['location'],status, data['comment'])
    my_incident.create_redflag(redflag)
    return jsonify({'data': [{ 'id':redflag.id , 'message': 'created redflag'}], 'status': 201}) ,201

@app.route('/api/v1/redflag', methods=['GET'])
def all_redflags():
    redflags = my_incident.fetch_all_redflags()
    if not redflags:
        return jsonify({'message': ' no flags found', 'status' : 404}) ,404
    return jsonify({'data':redflags, 'status': 200})
 
@app.route('/api/v1/redflag/<int:id>', methods=['GET'])
def specific_redflag(id):
    specific_flag = my_incident.fetch_specific_flag(id)
    if not specific_flag:
        return jsonify({'message': 'flag not found', 'status': 404}), 404
    return jsonify({'data': specific_flag, 'status': 200})

@app.route('/api/v1/redflag/<int:id>/location', methods=['PATCH'])
def edit_location(id):
        new_location = request.get_json()['location']
        redflag = my_incident.edit_location(id, new_location)
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404}) ,404
        return jsonify({'data':[{'id':id, 'message': \
         'Updated red-flag record location'}], 'status': 200})

@app.route('/api/v1/redflag/<int:id>/comment', methods=['PATCH'])
def edit_comment(id):
        data = request.get_json()
        redflag = my_incident.edit_comment(id, data['comment'])
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404}) ,404    
        return jsonify({'data':[{'id':id, \
        'message': "Updated red-flag records comment"}], 'status': 200})

@app.route('/api/v1/redflag/<int:id>', methods=['PUT'])
def edit_redflag(id):
        data = request.get_json()
        redflag = my_incident.edit_redflag(id, data['incidentType'], data['location'], data['comment'])
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404})
       
        return jsonify({'redflag': redflag[0]})

@app.route('/api/v1/redflag/<int:id>', methods=['DELETE'])
def remove_redflag(id):
    flag= my_incident.delete_redflag(id)
    if not flag:
        return jsonify({'message': 'flag not found', 'status': 400}), 404 
    return jsonify({'data':[{'id': id , 'message': 'redflag has been deleted'}], 'status': 200})


@app.route('/api/v1/redflag/<int:id>/status', methods=['PATCH'])
def update_status(id):
    new_status= request.get_json()['status']
    updated_status= my_incident.updateStatus(id , new_status)
    if not updated_status:
        return jsonify ({'message': 'flag not found', 'status': 404}), 404
    return jsonify({'data':[{'id': id , 'message': 'redflag status  has been updated to' +" "+ new_status}], \
    'status': 200 })


@app.route('/api/v1/user/register', methods=['POST'])  
def registerUser():
    data= request.get_json()
    if request.method == 'POST':
        data= request.get_json()
        if not request.json or not 'firstname' in data or not 'lastname' in data or not 'email' in data\
         or not 'tel' in data or not 'password' in data or not 'IsAdmin' in data:
            return jsonify({'message': 'bad request' , 'status': 404})
        user = User(data['firstname'], data['lastname'],data['othernames'], \
        data['username'], data['password'],data['email'], data['tel'], data['registered_date'], data['IsAdmin']) 
        my_incident.add_user(user)    
        return jsonify({'user': user.__dict__ , 'status': 200 })  
    return jsonify({'message': 'bad request' , 'status': 404})    

@app.route('/api/v1/user/login', methods=['GET', 'POST'])  
def login():
    data = request.get_json()
    if request.method == 'POST':
        if 'username' in data and 'password' in data:
            a_user= UserLogin(data['username'], data['password'])
            person = my_incident.loginuser(a_user)
            if person:
                return jsonify({'message': 'youre logged in'})
            return jsonify({'message': 'please register first'})  
        return jsonify({'message': ' Some fields are missing' ,'status': 400})      
    return jsonify({'message': 'login'})    

@app.route('/api/v1/user/<int:id>', methods=['GET'])
def fetch_redflags_for_user(id):
    all_redflags_by_specificUser = [redflag for redflag in incidents_list if redflag['createdby']== id]
    return jsonify({'redfalgs': all_redflags_by_specificUser})



if __name__== '__main__':
    app.run(debug=False)


