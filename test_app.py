import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors, db
from flask import request

# Tokens  (not worked for me )
# ASSTNT_TOKEN = os.environ['ASSISTANT_TOKEN']
# DIRECTOR_TOKEN = os.environ['DIRECTOR_TOKEN']
# PRODUCER_TOKEN = os.environ['PRODUCER_TOKEN']

ASSTNT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRHTWsxU3l3c0Q3TlVVYk5BYmY2OCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzN2YyOWNmYjM3ZDAwMDY4MjYxZGNlIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTc4MDYsImV4cCI6MTYxNDgwNDIwNiwiYXpwIjoickluOFU4eHoycHhHYk5wMkNYN1RGY2hCdmhndHMzMEQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.IQV_nzcjA8HmbltK_gff0nbxIaY8u2n7SVG0l82-Ssvv8hJIoaq2Fdq41DYuz2YPYBBVFXKcDb6CQcMc4I7nr-LuGsBbsUPo04UvDPRW81FpeIB3cphm2Io2cuDLsaeldXSOstN87wAmC0DGuGWGZgGS3ZQm8YYFCw_FxcMYpP1t8YW9f6YJwaIIYkNnj_y6nx6kLV4NNkwfm1p2DjcuxRx2EHbARdaT3hN5VGjpRni8vH2vqTf0RWY0q73aUa4lt4TPwWKJQz5c2iam_ySunkoUE35Riecu9qgE_PX-tPn9VNFSPWjW7y9jhpn21NA9abuAn2glRD3PSVxF4pE3UA'
DIRECTOR_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRHTWsxU3l3c0Q3TlVVYk5BYmY2OCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzN2YyOWNmYjM3ZDAwMDY4MjYxZGNlIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTc3MTIsImV4cCI6MTYxNDgwNDExMiwiYXpwIjoickluOFU4eHoycHhHYk5wMkNYN1RGY2hCdmhndHMzMEQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.08zlxURTwZTkD_5he4omSbPQjbzAtEEn2la6l4LgolAWeoj1ST4YrlA6OjOLZlS3mmCaFrUFYF9CrtifCdOgpHpviwc-r_ZKy-xu8PkOhszQvwmxjx5uBK5cVN_rpvevp-Nd2gvfT6i7Mx8EW9YIbZ9_iopPdo9PgTAofCRB5gb7yC50PzZKbV3v6G4WvKjRLP258WWawKqB6_rYeIr6fzgXFXThQAy8BNIzVLiIjRD1E4Owa8CfmLV3wZgIfOvUAHSuydvez7jPXy008ChKQNmTrtmz6Go4LHhmEhh_QtmvptUzej6bEx2dWx6jdhVHDUx_hBdSw818ktLp89SdXA'
PRODUCER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRHTWsxU3l3c0Q3TlVVYk5BYmY2OCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzN2YyOWNmYjM3ZDAwMDY4MjYxZGNlIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTQ3MTc0NTMsImV4cCI6MTYxNDgwMzg1MywiYXpwIjoickluOFU4eHoycHhHYk5wMkNYN1RGY2hCdmhndHMzMEQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.bQEeV4zsJbB_SZb9U4auwIRVdDtUv34ZGwt0ZeLq5kGT2zN0DfALMrjKqHSK8s7UIl_CKjuw6FuOewzgSKQSzy04_lXZeMO73gjKCW3K-ihd4tP_0DDAf41FTFmmkREiBt3QJCXahbZuo06njLyQmQcU5zgxa0hG7kvKj19xSDzhtzQTVgPLfQF5IHSUzuTenHCPtqMyi5JXUmqm46xAwwmzGBV6ZwC2IwFZpdu3YNdK8jfptKJRWMAKZZ0Az7kIAT74OSiDj6V5QnYStmdKp5semz6vSnnvZ11rGG_gWAUcCgxUxXozQmJiROek6w7BqJRENohqu0aBd3J6hYe_YQ'




class CastiongAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client 
        #self.database_path = os.environ['DATABASE_URL']
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'zeronyuuki23')  
        self.DB_NAME = os.getenv('DB_NAME', 'capstone')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    ##################### Movies testing ####################
    
    #test for successful operation to get movies  
    def test_get_movies(self):
        header ={"Authorization": "Bearer " + ASSTNT_TOKEN}
        #get endpoint (response) 
        res = self.client().get('/movies', headers=header) 
        #data of the response (loaded in JSON format)
        res_data = json.loads(res.data)
        #make sure satus code is 200 (OK)
        self.assertEqual(res.status_code, 200)
        #make sure succes is True
        self.assertEqual(res_data['success'], True)
        

    #test for get movies without permission (unauthorized)
    def test_get_movies_401(self):
        res = self.client().get('/movies') 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)


    #test for patch movies for director role (authorized)
    # def test_modify_movies(self):
    #     patched_movie={
    #     'title':"jumanji",
    #     'release_year':1995
    #     }
    #     header ={'Authorization': "Bearer {}".format(DIRECTOR_TOKEN)}
    #     res = self.client().patch('/movies/1', headers=header, json=patched_movie) 
    #     res_data = json.loads(res.data)
    #     print(res)
    #     print(res_data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res_data['success'], True)

    #test for patch movies for assistant role (unauthorized)
    def test_modify_movies_401(self):
        patched_movie={
        'title':"jumanji",
        'release_year':1995
        }
        header ={'Authorization': "Bearer {}".format(ASSTNT_TOKEN)}
        res = self.client().patch('/movies/1', headers=header, json=patched_movie) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)

     #test for post movies for producer role (authorized)
    def test_post_movies(self):
       
        new_movie ={
        'title':"Mulan",
        'release_year':2020

        }
        header ={'Authorization': "Bearer {}".format(PRODUCER_TOKEN)}
        #auth_header=request.headers['Authorization']
        #print(header)
        res = self.client().post('/add-movie', headers=header, json=new_movie)
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)


    #test for post movies for director role (unauthorized)
    def test_post_movies_401(self):
        new_movie ={
        'title':"Mulan",
        'release_year':2020

        }
        header ={'Authorization': "Bearer {}".format(DIRECTOR_TOKEN)}
        res = self.client().post('/add-movie', headers=header, json=new_movie) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)
     
  
    
    #test for delete movies for producer role (authorized)
    def test_delete_movies(self):
        header ={'Authorization': "Bearer {}".format(PRODUCER_TOKEN)}
        res = self.client().delete('/movies/1', headers=header) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)


    #test for delete movies for assistant role (unauthorized)
    def test_delete_movies_401(self):
        header ={'Authorization': "Bearer {}".format(ASSTNT_TOKEN)}
        res = self.client().delete('/movies/1', headers=header) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)

    
   
    ######################### Actors testing #############################
    # test for get actors for assistant (authorized)
    def test_get_actors(self):
        header ={'Authorization': "Bearer {}".format(ASSTNT_TOKEN)}
        res = self.client().get('/actors', headers=header) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)

    #test for get actors without permission (unauthorized)
    def test_get_actors_401(self):
        res = self.client().get('/actors') 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)


    #test for patch actors for director (authorized)
    # def test_modify_actors(self):
    #     new_actor={
    #     'name':"Dwayne Johnson",
    #     'age':48,
    #     'gender':'m'
    #     }
    #     header ={'Authorization': "Bearer {}".format(DIRECTOR_TOKEN)}
    #     res = self.client().patch('/actors/1', headers=header, json=new_actor) 
    #     res_data = json.loads(res.data)
    #     print(res)
    #     print(res_data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res_data['success'], True)

    #test for patch actors for assistant (unauthorized)
    def test_modify_actors_401(self):
        new_actor={
        'name':"Dwayne Johnson",
        'age':48,
        'gender':'m'
        }
        header ={'Authorization': "Bearer {}".format(ASSTNT_TOKEN)}
        res = self.client().patch('/actors/1', headers=header, json=new_actor) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)


    #test for post actors for director (authorized)
    def test_post_actors(self):
        new_actor={
        'name':"Jason Statham",
        'age':53,
        'gender':'m'
        }
        header ={'Authorization': "Bearer {}".format(DIRECTOR_TOKEN)}
        res = self.client().post('/add-actor', headers=header, json=new_actor) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)


    #test for post actors for assistant (unauthorized)
    def test_post_actors_401(self):
        new_actor={
        'name':"Jason Statham",
        'age':53,
        'gender':'m'
        }
        header ={'Authorization': "Bearer {}".format(ASSTNT_TOKEN)}
        res = self.client().post('/add-actor', headers=header, json=new_actor) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)

    

     #test for delete actors for director (authorized)
    def test_delete_actors(self):
        header ={'Authorization': "Bearer {}".format(DIRECTOR_TOKEN)}
        res = self.client().delete('/actors/1', headers=header) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['success'], True)


    #test for delete actors for assistant (unauthorized)
    def test_delete_actors_401(self):
        header ={'Authorization': "Bearer {}".format(ASSTNT_TOKEN)}
        res = self.client().delete('/actors/1', headers=header) 
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
