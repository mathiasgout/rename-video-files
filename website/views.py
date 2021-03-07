from flask import Blueprint, render_template, request, redirect, url_for, session, flash

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():

    # Enlever de la memoire "file_names" et "renaming_type"
    if request.method == "GET":
        session.pop("file_names", None)
        session.pop("renaming_type", None)
        

    if request.method == "POST":
        file_names = request.form.getlist("pickfiles")
        renaming_type = request.form.get("renaming_type")

        # pour garder en mémoire la variable "file_names"
        session["file_names"] = file_names 

        # Vérification 
        if not file_names[0]:
            flash("Sélectionner au moins un fichier.", category="error")
        elif renaming_type == "Film" and len(file_names) > 1:
            flash("Impossible de renommer plus d'un film à la fois.", category="error")
        else:
            session["renaming_type"] = renaming_type
            return redirect(url_for("views.info"))

    return render_template("home.html")


@views.route("/info", methods=["GET", "POST"])
def info():

    # Pour checker si on est passé par "/"
    if session.get("file_names") is None:
        return redirect(url_for("views.home"))

    file_names = session.get("file_names")
    renaming_type = session.get("renaming_type")
    
    if request.method == "POST":

        titre = request.form.get("titre")
        season = request.form.get("season")

        # dictionnaire -> {nom des episodes : numéro de l'épisode}
        movies_dict = {}
        for key, value in request.form.items():
            if key not in ["titre", "lang", "season"]:
                movies_dict[key] = value

        if len(titre) < 1 or len(titre) > 100:
            flash("Longueur du titre non valable.", category="error")
        elif not season:
            flash("Veuiller renseigner un numéro de saison.", category="error")
        for value in movies_dict.values():
            if not value:
                flash("Veuiller renseigner l'ensemble des numéros des épisodes.", category="error")
                break

    return render_template("info.html", renaming_type=renaming_type, file_names=file_names)
