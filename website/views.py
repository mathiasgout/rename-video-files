from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        print(request.form.getlist("pickfiles"))

        return redirect(url_for("views.infos"))

    return render_template("home.html")


@views.route("/infos")
def infos():
    return render_template("infos.html")