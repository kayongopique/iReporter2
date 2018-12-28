from flask import Flask, jsonify, request
from datetime import datetime
from api import app
from api.models.models import Incident, incidents_list, users, User

# from api.models.incident import IncidentArray
 

# my_incident = IncidentArray()


@app.route('/api/v1/redflag', methods=['POST'])
def create_redflag():
    data = request.get_json() 
      
    if not data  or not data['incidentType'] or not data['location']\
     or not data['comment']:
        return jsonify({'message': 'bad request', 'status': 404}), 404
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

@app.route('/api/v1/redflag', methods=['POST'])  
def registerUser():
    data= request.get_json()
    if not data or not data['firstname'] or not data['lastname'] or not data['email'] or not data['tel'] or not data['password']:
         return jsonify({'message': 'bad request' , 'status': 404})
    user = User(id, data[firstname], data['lastname'],data['othernames'], \
    data['username'], data['password'],data['email'], data['registered_date'], data['isAdmin'])     
    return jsonify({'user': user.__dict__ , 'status': 200 })     

# # @app.route('/redflag/<int:user_id>', methods=['GET'])
# # def fetch_redflags_for_user(user_id):
    
# #     all_redflags = [redflag for redflag in Redflags if redflag['user_id']== user_id]
# #     return jsonify({'redfalgs': all_redflags})



if __name__== '__main__':
    app.run(debug=False)


