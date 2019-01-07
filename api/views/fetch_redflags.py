# from flask import Flask,Blueprint, jsonify, request
# from api.views.create_redflag import IncidentArray
# fetch_redflags_blueprint = Blueprint('fetch_redflags_blueprint' ,__name__)
# my_incident = IncidentArray()



# @fetch_redflags_blueprint.route('/redflag', methods=['GET'])
# def all_redflags():
#     redflags = my_incident.fetch_all_redflags()
#     if not redflags:
#         return jsonify({'message': ' no flags found', 'status' : 404}) ,404
#     return jsonify({'data':redflags, 'status': 200})
 
# @fetch_redflags_blueprint.route('/redflag/<int:id>', methods=['GET'])
# def specific_redflag(id):
#     specific_flag = my_incident.fetch_specific_flag(id)
#     if not specific_flag:
#         return jsonify({'message': 'flag not found', 'status': 404}), 404
#     return jsonify({'data': specific_flag, 'status': 200})