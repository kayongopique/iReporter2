
import unittest
import json
from api import app
from api.views import views
from api.models.models import Incident


class TestRedflag(unittest.TestCase):
     def setUp(self):
          self.app_tester=app.test_client(self)
          
          self.incident1= {"username":"david",\
          "incidentType": "redflag",\
           "location": "gayaza", \
          "comment": "please check it out"}
          
          self.incident2= {"username":"davidpique",\
          "incidentType": "redflag",\
           "location": "kampala", \
          "comment": "please check it out"}
          
          self.incident3= {"username":"davidk",\
          "incidentType": "redflag",\
           "location": "entebbe", \
          "comment": "please check it out"}


     def test_post_empty_redflag(self):
          input_data = {}
          response=self.app_tester.post('/api/v1/redflag', json=input_data )
          self.assertEqual(response.status_code, 404)
          self.assertIn('Some fields are empty, please cross check', str(response.data))

     # def test_get_empty_redflag(self):
     #      input_data = {}
     #      response=self.app_tester.get('/api/v1/redflag', json=input_data )
     #      response = self.app_tester.get('/api/v1/redflag')
     #      self.assertEqual(response.status_code, 404)
     #      self.assertIn('no flags found', str(response.data))       
          
          
     def test_post_redflag(self):
          response = self.app_tester.post('/api/v1/redflag', json= self.incident1)
          self.assertEqual(response.status_code, 201)
          self.assertIn('created redflag', str(response.data))

     

     def test_get_redflag(self):
          res = self.app_tester.post('/api/v1/redflag', json= self.incident2)
          self.assertEqual(res.status_code, 201)
          self.assertIn('created redflag', str(res.data))
          response = self.app_tester.get('/api/v1/redflag')
          self.assertEqual(response.status_code, 200)
          self.assertIn('please check it out', str(response.data))  
     
     
     def test_get_nonExistingSpecific_redflag(self):
          response = self.app_tester.get('/api/v1/redflag/15')
          self.assertEqual(response.status_code, 404)
          self.assertIn('flag not found', str(response.data))   

     def test_get_specific_redflag(self):
          res = self.app_tester.post('/api/v1/redflag', json= self.incident2)
          self.assertEqual(res.status_code, 201)
          self.assertIn('created redflag', str(res.data))
          response = self.app_tester.get('/api/v1/redflag/1')
          self.assertEqual(response.status_code, 200)
           

     def test_edit_nonExistingSpecific_redflagLocation(self):
          response = self.app_tester.patch('/api/v1/redflag/20/location', json ={"location": "jinja"})
          self.assertEqual(response.status_code, 404)
          self.assertIn('flag not found', str(response.data)) 

     def test_edit_Specific_redflagLocation(self):
          res = self.app_tester.post('/api/v1/redflag', json= self.incident3)
          self.assertEqual(res.status_code, 201)
          response = self.app_tester.patch('/api/v1/redflag/1/location', json ={"location": "jinja"})
          self.assertEqual(response.status_code, 200)
          self.assertIn('Updated red-flag record location', str(response.data))      

     
     def test_edit_nonExistingSpecific_redflagComment(self):
          response = self.app_tester.patch('/api/v1/redflag/7/comment', json ={"comment": "check out"})
          self.assertEqual(response.status_code, 404)
          self.assertIn('flag not found', str(response.data))   

     def test_edit_Specific_redflagComment(self):
          res = self.app_tester.post('/api/v1/redflag', json= self.incident3)
          self.assertEqual(res.status_code, 201)
          response = self.app_tester.patch('/api/v1/redflag/1/comment', json ={"comment": "check out"})
          self.assertEqual(response.status_code, 200)
          self.assertIn('Updated red-flag records comment', str(response.data))        

     def test_delete_no_redflag(self):
          response = self.app_tester.delete('/api/v1/redflag/1')
          self.assertEqual(response.status_code, 404)
          self.assertIn('flag not found', str(response.data))  

     def test_delete_redflag(self):
          res = self.app_tester.post('/api/v1/redflag', json= self.incident3)
          self.assertEqual(res.status_code, 201)
          response = self.app_tester.delete('/api/v1/redflag/1')
          self.assertEqual(response.status_code, 200)
          self.assertIn('redflag has been deleted', str(response.data))  

     def test_update_status(self):
          res = self.app_tester.post('/api/v1/redflag', json= self.incident3)
          self.assertEqual(res.status_code, 201)
          response = self.app_tester.patch('/api/v1/redflag/1/status', json ={"status": "rejected"})
          self.assertEqual(response.status_code, 200)
          self.assertIn('rejected', str(response.data))      



    














     



     def tearDown(self):
          pass   
     

     
          
                     
     