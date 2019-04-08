from flask import jsonify, render_template, make_response, current_app
from datetime import date ,datetime
import uuid
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from api import Create_app
import psycopg2
import psycopg2.extras as ireport
from api import Create_app
from api import mail



class IncidentController:

    # def __init__(self):
        # database_url = app.config['DATABASE_URL']
        # parsed_url = urlparse(database_url)
        # dbname = parsed_url.path[1:]
        # user = parsed_url.username
        # host parsed_url.hostname
       # password = parsed_url.password
    # port parsed_url.port
    connection = psycopg2.connect(
           database ="ireporterdb",
           user ="postgres",
           password ="david",
           host ="localhost",
           port ="5432"
        )
    print(connection)
    connection.autocommit = True
    cursor = connection.cursor(cursor_factory = ireport.RealDictCursor)
    # drop_incident_table="DROP TABLE users cascade"
    # cursor.execute(drop_incident_table) 
    users_table = "CREATE TABLE IF NOT EXISTS users(user_id serial PRIMARY KEY,\
    firstname varchar(50),lastname varchar(50),\
    othernames varchar(50),username varchar(50),password varchar(250),email varchar(50),tel varchar(50),\
    registeredDate varchar(50),IsAdmin varchar(50));"
    cursor.execute(users_table)
    incident_table ="CREATE TABLE IF NOT EXISTS incidents(id serial PRIMARY KEY,\
        createdby INTEGER REFERENCES users(user_id),createdon varchar(50),incidentType varchar(50),location varchar(50),status varchar(50),\
        comment varchar(100));"
    cursor.execute(incident_table)
    grades_table = "CREATE TABLE IF NOT EXISTS grades(student_id serial PRIMARY KEY, \
    studentno varchar(50),maths INTEGER,eng INTEGER,\
    lug INTEGER,chem int);"
    cursor.execute(grades_table)
    
        
    
    # Create tables

    # def create_tables(self):

    #     """ method creates tables """

    #     incident_table ="CREATE TABLE IF NOT EXISTS incidents(id serial PRIMARY KEY,\
    #     createdby varchar(50),createdon varchar(50),incidentType varchar(50),status varchar(50),\
    #     comment varchar(100));"
    #     self.cursor.execute(incident_table)
        


    def drop_tables(self):
        """ method deletes tables """

        drop_incident_table="DROP TABLE incident_table cascade"
        self.cursor.execute(drop_incident_table) 

    def create_grade(self,grade):
        self.cursor.execute("INSERT INTO grades(studentno,\
        ,maths,eng,lug,chem)VALUES\
        (%s,%s,%s,%s,%s);", (grade.studentno,grade.maths,\
        grade.eng,grade.lug,grade.chem))

    def sendmail(self,to,subject,user):
        msg= Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,\
        sender =current_app.config['MAIL_SENDER'],recipients = [to]) 
        msg.body = make_response('new user'+ user + 'created' )
        msg.body = "new user"+ user + "created"
        mail.send(msg)
        return True

    def create_redflag(self,incident):
        self.cursor.execute("INSERT INTO incidents(createdby,\
        createdon,incidentType,location,status,comment)VALUES\
        (%s,%s,%s,%s,%s,%s);", (incident.createdby,incident.createdon,\
        incident.incidentType,incident.location,incident.status,incident.comment))
        
    
    def fetch_all(self,tablename):
        """fetch all from database tables"""
        query= ("SELECT * FROM %s;") %(tablename)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows
    

    def fetch_specific_flag(self,tablename, flag_id):
        """fetch one from the database table incidents"""
        query = ("SELECT * FROM %s WHERE id = '%s';") %(tablename,flag_id)
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row

    def fetch_all_for_user(self,column,user_id):
        query = ("SELECT * FROM incidents WHERE %s = %s;") %(column,user_id) 
        self.cursor.execute(query)
        all_userflags = self.cursor.fetch_all() 
        return all_userflags  

    
    def edit_comment(self,tablename,column, flag_id, comment):
        """updates the comment field in the databse"""
        query = ("SELECT * FROM %s WHERE id = %s;") %(tablename,flag_id)
        self.cursor.execute(query)
        specific_flag = self.cursor.fetchone()
        
        if not specific_flag:
            return []
        else:
            if specific_flag['status']== 'draft':
                query= ("UPDATE %s SET %s = '%s' WHERE id = %s;")\
                 %(tablename,column,comment,flag_id)
                self.cursor.execute(query)

                return specific_flag
            return specific_flag[status]    
            
            
    def edit_location(self,tablename,column, flag_id, location):

        """updates the location field in the databse"""
        query = ("SELECT * FROM %s WHERE id = %s;") %(tablename,flag_id)
        self.cursor.execute(query)
        specific_flag = self.cursor.fetchone()
        
        if not specific_flag:
            return []
        else:
            if specific_flag['status']== 'draft':
                query= ("UPDATE %s SET %s = '%s' WHERE id = %s;")\
                 %(tablename,column,location,flag_id)
                self.cursor.execute(query)
                return specific_flag
            return specific_flag['status']    
        


    def delete_redflag(self,tablename, flag_id):
        """deletes a field in the database"""
        query = ("SELECT * FROM %s WHERE id = %s;") %(tablename,flag_id)
        self.cursor.execute(query)
        specific_flag = self.cursor.fetchone()
        
        if not specific_flag:
            return []
        query= ("DELETE FROM %s WHERE id = %s;")\
         %(tablename,flag_id)
        self.cursor.execute(query)
        return specific_flag
        

    def add_user(self, user):
        """registers a new_user"""
        query =("SELECT * FROM %s WHERE %s = '%s';") %('users', 'email',user.email)
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        if  not users:
            self.cursor.execute("INSERT INTO users(firstname,\
            lastname,othernames,username,password,email,tel,registeredDate,IsAdmin) VALUES\
            (%s,%s,%s,%s,%s,%s,%s,%s,%s);", (user.firstname,user.lastname,\
            user.othernames,user.name,user.password,\
            user.email,user.tel,user.registered,user.IsAdmin))
            return user
        return False

#promote user to be admin
    def promote_user(self, user_id):
        query = ("SELECT * FROM users WHERE id = user_id;")
        self.cursor.execute(query)
        user = self.cursor.fetchone
        if not user:
            return None
        user.IsAdmin = True
        return True  


    def loginuser(self, userInfo):
        query =("SELECT user_id, username, password FROM users;")
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        for user in users:
            if user['username'] != userInfo.username:
                return False
            if check_password_hash(user['password'], userInfo.password):
                return user

    def fetch_specific_user(self,tablename, id):
        """fetch one from the database table users"""
        query = ("SELECT * FROM %s WHERE user_id = %s;") %(tablename,id)
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row

    def date_generator(self):
        return str(datetime.now())
        

    def get_status(self):
        return "draft"        

    def updateStatus(self,tablename,id, status):
        """updates the status field in the database"""
        query = ("SELECT * FROM %s WHERE id = %s;") %(tablename,flag_id)
        self.cursor.execute(query)
        specific_flag = self.cursor.fetchone()
        if not specific_incident:
            return []
        specific_incident['status']= status
        return specific_incident

    
