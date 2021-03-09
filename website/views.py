import os
import cv2
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():

    # Enlever de la memoire "file_names" et "renaming_type"
    if request.method == "GET":
        session["token"] = False

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
            session["token"] = True
            return redirect(url_for("views.info"))
            
    return render_template("home.html")


@views.route("/info", methods=["GET", "POST"])
def info():

    no_error = True

    file_names = session.get("file_names")
    renaming_type = session.get("renaming_type")

    # Pour checker si on est passé par "/"
    if request.method == "GET":
        if session.get("token"):
            session["token"] = False
        else:
            return redirect(url_for("views.home"))
    
    if request.method == "POST":
        
        dir_path = os.path.join("/home/mathias/Documents", request.form.get("path"))
        titre = request.form.get("titre")
        lang = request.form.get("lang")

        if renaming_type == "Série":
            season = int(request.form.get("season"))

            # dictionnaire -> {nom des episodes : numéro de l'épisode}
            movies_dict = {}
            for key, value in request.form.items():
                if key not in ["titre", "lang", "season", "path"]:
                    movies_dict[key] = int(value)

            # Vérification série
            for movie in file_names:
                if not os.path.exists(os.path.join(dir_path, movie)):
                    no_error = False
                    flash("Le chemin n'est pas bon.", category="error")
                    break
            if len(titre) < 1 or len(titre) > 100:
                no_error = False
                flash("Longueur du titre non valable.", category="error")
            if not season:
                no_error = False
                flash("Veuiller renseigner un numéro de saison.", category="error")
            for value in movies_dict.values():
                if not value:
                    no_error = False
                    flash("Veuiller renseigner l'ensemble des numéros des épisodes.", category="error")
                    break
        
        else:
            movies_dict = {file_names[0]:-1}

            # Vérification film
            if not os.path.exists(os.path.join(dir_path, file_names[0])):
                no_error = False
                flash("Le chemin n'est pas bon.", category="error") 
            if len(titre) < 1 or len(titre) > 100:
                no_error = False
                flash("Longueur du titre non valable.", category="error")

        # Renommage
        if no_error is True:
            new_files_name = []
            old_files_name = []
            new_title = titre.replace(" ", "-").lower()

            if renaming_type == "Film":
                old_file_path = os.path.join(dir_path, file_names[0])
                movie_infos = get_file_infos(old_file_path)

                new_file_name = f"{new_title}_{movie_infos['width']}x{movie_infos['height']}_{lang}_{movie_infos['size_mb']}MB.{movie_infos['video_format']}"
                new_files_name.append(new_file_name)
                old_files_name.append(file_names[0])

            if renaming_type == "Série":
                for serie, nb in movies_dict.items():
                    old_file_path = os.path.join(dir_path, serie)
                    movie_infos = get_file_infos(old_file_path)

                    new_file_name = f"{new_title}_S{season:02d}E{nb:02d}_{movie_infos['width']}x{movie_infos['height']}_{lang}_{movie_infos['size_mb']}MB.{movie_infos['video_format']}" 
                    new_file_path = os.path.join(dir_path, new_file_name)
                    new_files_name.append(new_file_name)
                    old_files_name.append(serie)

            session["dir_path"] = dir_path
            session["new_files_name"] = new_files_name
            session["old_files_name"] = old_files_name
            session["token"] = True

            return redirect(url_for("views.completed_actions"))

    return render_template("info.html", renaming_type=renaming_type, file_names=file_names)


@views.route("/completed-actions", methods=["GET", "POST"])
def completed_actions():

    # Pour checker si on est passé par "/" et "/info"
    if request.method == "GET":
        if session.get("token"):
            session["token"] = False
        else:
            return redirect(url_for("views.home"))

    dir_path = session.get("dir_path")
    new_files_name = session.get("new_files_name")
    old_files_name = session.get("old_files_name")

    if request.method == "POST":
        if request.form.get("ok_button") == "clicked":
            for i in range(len(new_files_name)):
                os.rename(os.path.join(dir_path, old_files_name[i]), os.path.join(dir_path, new_files_name[i]))
            flash("Fichiers renommés !", category="succes")
            return redirect(url_for("views.info"))
    
        elif request.form.get("cancel_button") == "clicked":
            flash("Fichiers non renommés.", category="error")
            return redirect(url_for("views.home"))

    return render_template("completed-actions.html", new_files_name=new_files_name, old_files_name=old_files_name)


def get_file_infos(file_path):
    """ Get infos about the video file """

    cv2video = cv2.VideoCapture(file_path)
    height = int(cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cv2video.get(cv2.CAP_PROP_FRAME_WIDTH))
    size_mb = int(os.path.getsize(file_path) / 10**6)
    video_format = file_path.split(".")[-1]

    return {"height":height, "width":width, "size_mb":size_mb, "video_format":video_format}