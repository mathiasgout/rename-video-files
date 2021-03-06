from flask import Flask

def create_app():
    """
    Initialisation de l'application
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dlezpf6o79fpdvfpe56fsf5d4gre"

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app