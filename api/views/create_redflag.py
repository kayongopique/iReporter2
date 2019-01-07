# from flask import Flask,Blueprint, jsonify, request
# from api.models.models import Incident

# from api.models.incident import IncidentArray
 
# create_redflag_blueprint = Blueprint('create_redflag_blueprint' ,__name__)
# my_incident = IncidentArray()


# @create_redflag_blueprint.route('/redflag', methods=['POST'])
# def create_redflag():
#     data = request.get_json() 
#     if not request.json or not 'incidentType' in data or not 'location' in data or not 'comment' in data:
#         return jsonify({'message': 'Some fields are empty, please cross check', 'status': 404}), 404
#     status = my_incident.get_status() 
#     id = my_incident.incidentId_generator()
#     owner = data['username']
#     createdby = my_incident.createdby(owner)
#     createdon = my_incident.incidentDate_generator()
#     redflag = Incident(id, createdby, createdon, data['incidentType'],data['location'],status, data['comment'])
#     my_incident.create_redflag(redflag)
#     return jsonify({'data': [{ 'id':redflag.id , 'message': 'created redflag'}], 'status': 201}) ,201
