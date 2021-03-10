from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Base de données User, UserMixin uniquement pour les bases de données User 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # id, clef primaire de la base de données User
    password = db.Column(db.String(150))
    id_name = db.Column(db.String(150), unique=True)
    renamed = db.relationship("Renamed") # pour identifier la relation entre les 2 jeux de données

class Renamed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    old_name = db.Column(db.String(1000))
    new_name = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func.now pour avoir l'heure de création automatique
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) # clef étrangère