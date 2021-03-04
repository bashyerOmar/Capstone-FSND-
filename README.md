# Capstone Final Project (Casting Agency )



## PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by open your terminal and run:

```bash
pip install -r requirements.txt
```
This will install all of the required packages within the `requirements.txt` file.


## Running the server

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
```windows (cmd)
set FLASK_APP=app.py
set FLASK_ENV=development
python -m flask run 
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` file to find the application. 



## Getting Started
Base URL: this application hosted on https://capstone-fsnd-bshayer.herokuapp.com/ 
Authentication: This application require authentication for all endpoints except index endpoint.


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message":Resource Not Found
}
```
The API will return seven error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
401:permission not found
403:Forbidden
405:method not allowed 
500: Server error


## API Endpoints

#### GET '/movies'
General:
- Fetches all movies from database  
- require authntication 
- Return success value and list of movies formmated as JSON 
```

{
    "movies": [
        {
            "id": 1,
            "release_year": 2017,
            "title": "Avatars"
        },
        {
            "id": 2,
            "release_year": 2019,
            "title": "crew"
        }
    ],
    "success": true
}
```

#### GET '/actors'
General:
- Fetches all actors from database  
- require authntication 
- Return success value and list of actors formmated as JSON 
```
{
    "actors": [
        {
            "age": 23,
            "gender": "F",
            "id": 1,
            "name": "Emy"
        },
        {
            "age": 48,
            "gender": "m",
            "id": 2,
            "name": "The Rock"
        }
    ],
    "success": true
}
}
```

#### POST '/add-movie'
General:
- insert (post) new movies to database  
- require authntication 
- Return success value and new movie added formmated as JSON 
```
{
    "movie": {
        "id": 3,
        "release_year": 2020,
        "title": "Mulan"
    },
    "success": true
}
```

#### POST '/add-actor'
General:
- insert (post) new actors to database  
- require authntication 
- Return success value and new actor added formmated as JSON
```
{
    "actor": {
        "age": 53,
        "gender": "m",
        "id": 3,
        "name": "Jason Statham"
    },
    "success": true
}
```

#### PATCH 'movies/1'
General:
- modify movie data based on id (id=1)
- require authntication 
- Return success value and movie after update formmated as JSON
```
{
    "movie": {
        "id": 1,
        "release_year": 1995,
        "title": "jumanji"
    },
    "success": true
}
```


#### PATCH 'actors/1'
General:
- modify actor data based on id (id=1)
- require authntication 
- Return success value and actor after update formmated as JSON
```
{
    "actor": {
        "age": 48,
        "gender": "m",
        "id": 1,
        "name": "Dwayne Johnson"
    },
    "success": true
}
```


#### DELETE 'movies/1'
General:
- remove movie with id=1 from database 
- require authntication 
- Return success value and id of the removed movie 
```
{
    "deleted": 1,
    "success": true
}
```

#### DELETE 'actors/1'
General:
- remove actor with id=1 from database 
- require authntication 
- Return success value and id of the removed actor
```
{
    "deleted": 1,
    "success": true
}
```


## Testing
To run the tests, open termianl and then run this command
```
python test_app.py
```
