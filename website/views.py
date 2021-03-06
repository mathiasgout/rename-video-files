from flask import Blueprint, render_template, request, redirect, url_for, session

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        file_names = request.form.getlist("pickfiles")

        # pour garder en mémoire la variable "file_names"
        session["file_names"] = file_names 
        return redirect(url_for("views.infos"))

    return render_template("home.html")


@views.route("/infos")
def infos():
    file_names = session["file_names"]
    print(file_names)
    return render_template("infos.html", file_names=file_names)