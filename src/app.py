"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    user_serialize = user.serialize()
    
    return jsonify(user_serialize), 200

@app.route('/users', methods=['GET'])
def handle_users():
    
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():
    
    request_body_user = request.get_json()
    new_user = User(username=request_body_user["username"], password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    
    request_body_user = request.get_json()
    
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    
    if "username" in request_body_user:
        user1.username = request_body_user["username"]
    if "password" in request_body_user:
        user1.password = request_body_user["password"]
    db.session.commit()
    
    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    
    return jsonify("OK"), 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    
    characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_characters), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    
    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_characters(characters_id):
    
    character = Characters.query.get(characters_id)
    if character is None:
        raise APIException('Character not found', status_code=404)
    character_serialize = character.serialize()
    
    return jsonify(character_serialize), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets(planets_id):
    
    planet = Planets.query.get(planets_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    planet_serialize = planet.serialize()
    
    return jsonify(planet_serialize), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
