import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies, db
from auth import AuthError, requires_auth

def create_app(test_config=None):
    
    # create and configure the app
      
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # ROUTES

    @app.route('/')
    def index():
       return 'Final Project "Casting Agency" '

    #################################################### Actor Endpoints #############################
    # get all actors, permision here for (Assistant , Director and producer)
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_all_actors(payload_token):
      # fetch all actors from db 
      all_actors=db.session.query(Actors).all()
    
      if all_actors is None:
        abort(404)
      else:
        # format actors to JSON 
        formmated_actors=[Actors.format(actor) for actor in all_actors]
        return jsonify({
            'success': True,
            'actors':formmated_actors
        }), 200 


    # add actor to db , permission here for ( Director and Producer)
    @app.route('/add-actor', methods=['POST'])
    @requires_auth('post:actors')
    def add_new_actor(payload_token):
        # get the data of actor as JSON
        actor_data = request.json

        if not actor_data:
             abort(400)

        name = actor_data["name"]
        age = actor_data["age"]
        gender = actor_data["gender"]

         
        # create new actor object
        new_actor=Actors(name=name, age=age, gender=gender) 
          # insert new actor to db 
        Actors.insert(new_actor) 
         
          # format actor to JSON 
        formmated_actor=Actors.format(new_actor) 
        return jsonify({
            'success': True,
            'actor':formmated_actor
          }), 200 

    # remove actor from db , permission here for ( Director and Producer)
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def remove_actor(payload_token, actor_id):

          
        actor_to_delete=db.session.query(Actors).filter(Actors.id == actor_id).one_or_none()
        if actor_to_delete is None:
            abort(404)
        
        Actors.delete(actor_to_delete)
        
        return jsonify({
               'success':True,
               'deleted':actor_id
          }), 200
         

    @app.route('/actors/<int:actor_id>',  methods=['PATCH'])
    # modify actor , permission here for ( Director and Producer)
    @requires_auth('patch:actors')
    def change_some_actor_data(payload_token, actor_id):

          # fetch data of the required actor
          actor_to_update=db.session.query(Actors).filter(Actors.id == actor_id).one_or_none()
          if not actor_to_update:
             abort(404)

          updated_actor_data=request.json
          if not updated_actor_data:
             abort(404)
          # check if there is new value for name
          if "name" in updated_actor_data:
            new_name=updated_actor_data["name"]
            #replace old name with new one 
            actor_to_update.name = new_name
          # check if there is new value for age 
          if "age" in updated_actor_data:
            new_age=updated_actor_data["age"]
            #replace old age with new one
            actor_to_update.age = new_age 
     
          # check if there is new value for gender
          if "gender" in updated_actor_data:
            new_gender=updated_actor_data["gender"]
            #replace old age with new one
            actor_to_update.gender = new_gender

          Actors.update(actor_to_update)
          formmated_actor=Actors.format(actor_to_update)
          return jsonify({
               'success':True,
               'actor':formmated_actor
          }), 200

    #################################################### Movie Endpoints #############################
    # get all movies, permision here for (Assistant , Director and producer)
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_all_movies(payload_token):
        # fetch all actors from db 
        all_movies=db.session.query(Movies).all()
        
        if all_movies is None:
               abort(404)
        else:
            # format movies to JSON 
            formmated_movies=[Movies.format(movie) for movie in all_movies]
            return jsonify({
                'success': True,
                'movies':formmated_movies
            }), 200 

      # add movie to db , permission here for Producer only
    @app.route('/add-movie', methods=['POST'])
    @requires_auth('post:movies')
    def add_new_movie(payload_token):
          #get the data of movie as JSON
          movie_data=request.json

          if not movie_data:
            abort(400)

          title = movie_data["title"]
          release_year= movie_data["release_year"]
          
          # create new movie object
          new_movie=Movies(title=title , release_year=release_year) 
          # insert new  movie to db 
          Movies.insert(new_movie) 
         
          # format movie to JSON 
          formmated_movie=Movies.format(new_movie) 
          return jsonify({
            'success': True,
            'movie':formmated_movie
          }), 200 

      # remove movie from db , permission here for Producer only
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def remove_movie(payload_token, movie_id):
          movie_to_delete=db.session.query(Movies).filter(Movies.id == movie_id).one_or_none()
          if movie_to_delete is None:
            abort(404)
        
          Movies.delete(movie_to_delete)
        
          return jsonify({
               'success':True,
               'deleted':movie_id
          }), 200
      

    @app.route('/movies/<int:movie_id>',  methods=['PATCH'])
    # modify actor , permission here for ( Director and Producer)
    @requires_auth('patch:movies')
    def change_some_movie_data(payload_token, movie_id):

          # fetch data of the required actor
          movie_to_update=db.session.query(Movies).filter(Movies.id == movie_id).one_or_none()
          if not movie_to_update:
             abort(404)

          updated_movie_data=request.json
          if not updated_movie_data:
             abort(400)
          # check if there is new value for title
          if "title" in updated_movie_data:
            new_title=updated_movie_data["title"]
            #replace old title with new one 
            movie_to_update.title = new_title
          # check if there is new value for release date 
          if "release_year" in updated_movie_data:
            new_release_year=updated_movie_data["release_year"]
            #replace old release date with new one
            movie_to_update.release_year = new_release_year 
     

          Movies.update(movie_to_update)
          formmated_movie=Movies.format(movie_to_update)
          return jsonify({
               'success':True,
               'movie':formmated_movie

            }), 200



    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False, 
          "error": 422,
          "message": "unprocessable"
          }), 422
               

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False, 
          "error": 404,
          "message": "resource not found"
          }), 404


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False, 
          "error": 400,
          "message": "Bad Request"
          }), 400


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
          "success": False,
          "error": 405,
          "message": "Method Not Allowed"
          }), 405

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
          "success": False, 
          "error": 500,
          "message": "internal server error"
          }), 500

    #to handle 403 and 401 
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code


    return app

app = create_app()

if __name__ == '__main__':
    app.run