from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # pour crypter les mdp
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"]) # pour que la route puisse accepter les requetes GET et POST
def login():
    if request.method == "POST":
        id_name = request.form.get("id_name")
        password = request.form.get("password")

        user = User.query.filter_by(id_name=id_name).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Connexion réussie !", category="succes")

                # connexion 
                login_user(user, remember=True)

                return redirect(url_for("views.home"))

            else:
                flash("Mot de passe incorrect.", category="error")
        else:
            flash("L'identifiant n'existe pas.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required # route inaccessible si aucun user connecté
def logout():
    # déconnexion
    logout_user()
    return redirect(url_for("auth.login"))