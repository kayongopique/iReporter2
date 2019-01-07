
from flask import Flask, jsonify, request
from api import app
from api.models.models import Incident

from api.models.incident import IncidentArray
 

my_incident = IncidentArray()


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