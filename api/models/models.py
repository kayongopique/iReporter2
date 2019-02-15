

class User:
    """
    Creates a user object for each user.
    """

    def __init__(self,firstname, lastname, othernames, username, password,\
     email, tel, registered_date, IsAdmin):
        self.firstname= firstname
        self.lastname= lastname
        self.othernames=othernames
        self.name = username
        self.password = password
        self.email = email
        self.tel = tel
        self.registered = registered_date
        self.IsAdmin= IsAdmin

   


class Incident:
    """
    Creates a incident object for each incident recieved.
    """

    def __init__(self,createdby,createdon, incidentType, location, status, comment ):
        self.createdby = createdby
        self.createdon=createdon 
        self.incidentType  = incidentType
        self.location = location
        self.status = status
        self.comment = comment
    
    def to_json(self ):
        return {  'id': self.id, 'createdby': self.createdby, 'createdon': self.createdon, \
        'incidentType': self.incidentType, 'location': self.location ,'status': self.status, \
             'comment': self.comment }
   
class UserLogin:
    def __init__(self, username, password):
        self.username = username
        self.password =password


class  Student:
    """creates a student object for every student"""
    def __init__(self,studentno,firstname,surname):
        self.id = studentno
        self.firstname =firstname
        self.surname =surname

class StudentGrade:
    """create object for every grade"""
    def __init__(self,studentno, maths,eng,lug,chem ):
        self.studentno = studentno
        self.maths = maths
        self.eng = eng 
        self.lug = lug  
        self.chem = chem   
        