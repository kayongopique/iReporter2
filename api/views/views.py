from flask import Flask, jsonify, request
from datetime import datetime
from api import app
from api.models.models import Incident, incidents_list, users, User, UserLogin

# from api.models.incident import IncidentArray
 

# my_incident = IncidentArray()


@app.route('/api/v1/redflag', methods=['POST'])
def create_redflag():
    data = request.get_json() 
    if not request.json or not 'incidentType' in data or not 'location' in data or not 'comment' in data   or not 'createdby' in data\
     or not 'createdon' in data :
        return jsonify({'message': 'Some fields are empty, please cross check', 'status': 404}), 404
    # status = my_incident.get_status() 
    # id = my_incident.incidentId_generator()
    # createdby = my_incident.userId_generator()
    # createdon = my_incident.incidentDate_generator()
    redflag = Incident(id,data['createdby'], data['createdon'],  data['incidentType'],\
     data['location'],data['status'], data['comment'])
    # my_incident.create_redflag(redflag)
    incidents_list.append(redflag.__dict__)
    return jsonify({'data': [{ 'redflag':redflag.__dict__ , 'message': 'created redflag'}], 'status': 201}) ,201

@app.route('/api/v1/redflag', methods=['GET'])
def all_redflags():
    redflags = incidents_list
    if not redflags:
        return jsonify({'message': ' no flags found', 'status' : 404}) ,404
    return jsonify({'data':redflags, 'status': 200})
 
@app.route('/api/v1/redflag/<int:id>', methods=['GET'])
def specific_redflag(id):
    specific_flag = [redflag for redflag in incidents_list  if redflag['id']==id]
    if not specific_flag:
        return jsonify({'message': 'flag not found', 'status': 404}), 404
    return jsonify({'data': specific_flag[0], 'status': 200})

@app.route('/api/v1/redflag/<int:id>/location', methods=['PATCH'])
def edit_location(id):
        data = request.get_json()
        redflag =[redflag for redflag in incidents_list if redflag['id']==id]
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404}) ,404
        redflag[0]['location']= data['location']
        return jsonify({'data':[{'id':redflag[0]['id'], 'message': \
         'Updated red-flag record location'}], 'status': 200})

@app.route('/api/v1/redflag/<int:id>/comment', methods=['PATCH'])
def edit_comment(id):
        data = request.get_json()
        redflag =[redflag for redflag in incidents_list if redflag['id']==id]
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404}) ,404    
        redflag[0]['comment']= data['comment']
        return jsonify({'data':[{'id':redflag[0]['id'], \
        'message': "Updated red-flag records comment"}], 'status': 200})

@app.route('/api/v1/redflag/<int:id>', methods=['PUT'])
def edit_redflag(id):
        data = request.get_json()
        redflag =[redflag for redflag in incidents_list if redflag['id']==id]
        if not redflag:
             return jsonify({'message': 'flag not found', 'status': 404})
        redflag[0]['id']= data['id']
        redflag[0]['createdon']= data['createdon']
        redflag[0]['redflag']= data['redflag']
        redflag[0]['createdby']= data['createdby']
        redflag[0]['location']= data['location']
        redflag[0]['comment']= data['comment']
        return jsonify({'redflag': redflag[0]})

@app.route('/api/v1/redflag/<int:id>', methods=['DELETE'])
def remove_redflag(id):
    flag= [redflag for redflag in incidents_list if redflag['id']==id]
    if not flag:
        return jsonify({'message': 'flag not found', 'status': 400}), 404 
    incidents_list.remove(flag[0])
    return jsonify({'data':[{'id': flag[0]['id'] , 'message': 'redflag has been deleted'}], 'status': 200})

@app.route('/api/v1/user/register', methods=['POST'])  
def registerUser():
    data= request.get_json()
    if request.method == 'POST':
        data= request.get_json()
        if not request.json or not 'firstname' in data or not 'lastname' in data or not 'email' in data\
         or not 'tel' in data or not 'password' in data or not 'IsAdmin' in data:
            return jsonify({'message': 'bad request' , 'status': 404})
        user = User(id, data['firstname'], data['lastname'],data['othernames'], \
        data['username'], data['password'],data['email'], data['tel'], data['registered_date'], data['IsAdmin']) 
        users.append(user)    
        return jsonify({'user': user.__dict__ , 'status': 200 })  
    return jsonify({'message': 'bad request' , 'status': 404})    

@app.route('/api/v1/user/login', methods=['GET', 'POST'])  
def login():
    data = request.get_json()
    if request.method == 'POST':
        if 'username' in data and 'password' in data:
            user= UserLogin(data['username'], data['password'])
            person = [user for user in users if user.name == user.username and user.password==user.password]
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


