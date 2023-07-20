from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    login_status = db.Column(db.Boolean(), unique=False, nullable=True, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=True)
    eye_color = db.Column(db.String(80), unique=False, nullable=True)
    hair_color = db.Column(db.String(80), unique=False, nullable=True)
    

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(80), unique=False, nullable=True)
    terrain = db.Column(db.String(80), unique=False, nullable=True)
    

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    crew = db.Column(db.Integer, unique=False, nullable=True)
    model = db.Column(db.String(80), unique=False, nullable=True)
    manufacturer = db.Column(db.String(80), unique=False, nullable=True)
    

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship('User', lazy=True)

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            # "name": self.name,
            # do not serialize the password, its a security breach
        }