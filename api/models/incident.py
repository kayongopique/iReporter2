from api.models.models import Incident
from datetime import date ,datetime


class IncidentArray:
    
    
    def __init__(self):
        self.incident_array =[]
        self.users =[]

    
    def fetch_all_redflags(self):
       
        return self.incident_array

    
    def create_redflag(self, incident):
        new_incident = incident.to_json()
        self.incident_array.append(new_incident)
        return new_incident

    
    def fetch_specific_flag(self, id):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        return specific_flag[0]

    
    def edit_comment(self, id, comment):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        specific_flag[0]['comment'] =comment
        return specific_flag[0]
    
    
    def edit_location(self, id, location):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        specific_flag[0]['location'] =location
        return specific_flag[0]


    def delete_redflag(self, id):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        self.incident_array.remove(specific_flag[0])
        return specific_flag[0]

    
    def incidentId_generator(self):
        return len(self.incident_array) + 1


    def incidentDate_generator(self):
        return datetime.today

    def userId_generator(self):
        return len(self.users) + 1


    # def fetch_user_id(self, username):
    #     specific_user =[ user for user in self.users if user['username']== username]

    #     if specific_user:
    #         return specific_user[0].id

       
    #     return user_id

    def get_status(self):
        return "draft"        



