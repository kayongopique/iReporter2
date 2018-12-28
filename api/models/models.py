

incidents_list = []
users =[]


class User:
    """
    Creates a user object for each user.
    """

    def __init__(self, **kwargs):
        self.id =id
        self.firstname= firstname
        self.lastname= lastname
        self.othernames=othernames
        self.name = username
        self.password = password
        self.email = email
        self.tel = tel
        self.registered = registered_date
        self.IsAdmin= bool

   


class Incident:
    """
    Creates a incident object for each incident recieved.
    """

    def __init__(self, id,createdby, createdon, incidentType, location, status, comment ):
        self.id = len(incidents_list) +1
        self.createdby = createdby
        self.createdon= createdon
        self.incidentType  = incidentType
        self.location = location
        self.status = status
        self.comment = comment
    
    def to_json(self ):
        return {  'id': self.id, 'createdby': self.createdby, 'createdon': self.createdon, \
        'incidentType': self.incidentType, 'location': self.location ,'status': self.status, \
             'comment': self.comment }
   
