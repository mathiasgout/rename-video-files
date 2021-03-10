import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Définition de la base de donnée
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """
    Initialisation de l'application
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dlezpf6o79fpdvfpe56fsf5d4gre"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # pour enlever le warning
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}" # place ou se situe la base de données SQL Alchemy
    db.init_app(app) # initialisation de la base de données
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Création des bases de données lors du 1er lancement de l'app
    from .models import User, Renamed

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # page de redirection si aucun user connecté
    login_manager.login_message = "Identifiez-vous pour accéder à cette page."
    login_manager.init_app(app)

    # pour dire a flask comment se connecter
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Creation des bases de données si elles n'existent pas
def create_database(app):
    if not os.path.exists(os.path.join("website", DB_NAME)):
        db.create_all(app=app)
        print("Created Database !")