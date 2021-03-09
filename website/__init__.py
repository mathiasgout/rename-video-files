from flask import Flask, request

def create_app():
    """
    Initialisation de l'application
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dlezpf6o79fpdvfpe56fsf5d4gre"
    
    # Pour empecher ce reculer d'une page
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "public, no-cache, no-store, must-revalidate, post-check=0, pre-check=0, max-age=0"
        return response

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app