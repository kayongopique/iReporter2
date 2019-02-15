from flask import jsonify
from datetime import date ,datetime
from werkzeug.security import generate_password_hash, check_password_hash



class IncidentArray:
    
    incident_array =[]
    users =[]

    
    def create_redflag(self, incident):
        new_incident = incident.to_json()
        self.incident_array.append(new_incident)
        return new_incident

    
    def fetch_all_redflags(self):
       
        return self.incident_array
    

    def fetch_specific_flag(self, id):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        return specific_flag

    
    def edit_comment(self, id, comment):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        if not specific_flag:
            return []
        else:
            if specific_flag[0]['status']== 'draft':
                specific_flag[0]['comment'] = comment
                return specific_flag
            return specific_flag[0]['status']    
            
            
    
    
    def edit_location(self, id, location):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        if not specific_flag:
            return []
        else:
            if specific_flag[0]['status']== 'draft':
                specific_flag[0]['location'] = location
                return specific_flag
            return specific_flag[0]['status']    
        


    def delete_redflag(self, id):
        specific_flag= [incident for incident in self.incident_array if \
        incident['id']==id]
        if not specific_flag:
            return []
        self.incident_array.remove(specific_flag[0])
        return specific_flag

    def edit_redflag(self, id, incidentType, location, comment): 
        redflag =[redflag for redflag in self.incident_array if redflag['id']==id]
        redflag[0]['incidentType']= incidentType
        redflag[0]['location']= location
        redflag[0]['comment']= comment
        return redflag

    def add_user(self, user):
        if user.name in self.users:
            return "user with this username already exists"
        new_user = user
        self.users.append(new_user)
        return new_user 


#promote user to be admin
    def promote_user(self, id):
        user = [user for user in self.users if user.id ==id]

        if not user:
            return None
        user[0].IsAdmin = True
        return True  


    def fetch_all_users(self):
        users_lst=[]
        for users in self.users:
            users_lst.append(users.__dict__)
       
        return users_lst  

    def loginuser(self, userInfo):
        person = [user for user in self.users if user.name == userInfo.username]
        if not person:
            return False
        if check_password_hash(person[0].password, userInfo.password):
            return person

   
    def incidentId_generator(self):
        if len(self.incident_array) == 0:
            return 1
        return self.incident_array[-1]['id'] +1    


    def date_generator(self):
        return str(datetime.now())


    def createdby(self, username):
        specific_user =[ user for user in self.users if user.name== username]

        if specific_user:
            return specific_user.id
        return len(self.users) +1    
        

    def get_status(self):
        return "draft"        

    def updateStatus(self,id, status):
        specific_incident = [incident for incident in self.incident_array if incident['id']==id]
        if not specific_incident:
            return []
        specific_incident[0]['status']= status
        return specific_incident


