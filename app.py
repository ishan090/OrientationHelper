
import json
from flask import Flask, redirect, url_for, render_template, request, session, flash


data_path = "data/"
users = ["med", "it", "advancement", "frro"]
passwords = {
    "med": "medcenter",
    "it": "computer",
    "advancement": "blahblah",
    "frro": "why"
}


def get_data(name):
    """Gets data from json files (only)"""
    filepath = data_path + name
    with open(filepath) as f:
        data = json.load(f)
    return data


def dump_data(name, data):
    """Dumps data to json files (only)"""
    filepath = data_path + name
    with open(filepath, "w") as f:
        json.dump(data, f)


data_loaded = get_data("data.json")

app = Flask(__name__)
app.secret_key = "ishan"

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home", methods=["GET", "POST"])
def home():
    if not session.get("user"):
        return redirect("/login/")
    user = session["user"]
    if request.method == "POST":
        data_loaded[users.index(user)][1] = request.form["traffic"]
        dump_data("data.json", data_loaded)
    return render_template("home.html", user=user, locations=data_loaded)


@app.route("/login/", methods=["POST", "GET"])
def login():
    to_flash = ""
    if request.method == "POST":
        if request.form["username"] in users:
            user = request.form["username"]
            if request.form["pw"] == passwords[user]:
                session["user"] = request.form["username"]
                return redirect("/home")
            else:
                to_flash = "Invalid Password"
        else:
            to_flash = "Invalid Username"
    if to_flash:
        flash(to_flash)
    return render_template("login.html")

@app.route("/logout/")
def logout():
    if session["user"]:
        session["user"] = None
    return redirect("/login/")

@app.route("/traffic/")
def traffic():
    return render_template("traffic.html", locations=data_loaded)


app.run(host="0.0.0.0", debug=True)
