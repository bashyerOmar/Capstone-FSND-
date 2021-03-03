from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
import os

# DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
# DB_USER = os.getenv('DB_USER', 'postgres')  
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'zeronyuuki23')  
# DB_NAME = os.getenv('DB_NAME', 'capstone')  
# DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
#database_path = os.environ['DATABASE_URL'] # from heroku
self.database_path='postgres://jredwjddmefdux:793ae2f82281dc23f7ea165ff44f16cab5fbdf28c3f73fdc9c9351c3eaeaaf13@ec2-54-164-241-193.compute-1.amazonaws.com:5432/d6tjrcq4k614fq'
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()  
    # db.create_all()



class Movies(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    release_year = db.Column(db.Integer)
    


    def __init__(self, title, release_year):
	    self.title = title
	    self.release_year = release_year
    

    def insert(self):
	    db.session.add(self)
	    db.session.commit()
  
    def update(self):
	    db.session.commit()

    def delete(self):
	    db.session.delete(self)
	    db.session.commit()#7

    def format(self):
	    return {
	      'id': self.id,
	      'title': self.title,
	      'release_year': self.release_year
	      
	    }


class Actors(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    gender = db.Column(db.CHAR)
    #movie_id = db.Column(db.Integer, db.ForeignKey('Movies.id'), nullable=True)


    def __init__(self, name, age, gender):
	    self.name = name
	    self.age = age
	    self.gender = gender
    

    def insert(self):
	    db.session.add(self)
	    db.session.commit()
  
    def update(self):
	    db.session.commit()

    def delete(self):
	    db.session.delete(self)
	    db.session.commit()#7

    def format(self):
	    return {
	      'id': self.id,
	      'name': self.name,
	      'age': self.age,
	      'gender':self.gender
	     
	    }