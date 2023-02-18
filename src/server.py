from flask import Flask, redirect, render_template, session, request, jsonify, make_response
from flask_session import Session
import json
from hashlib import sha256
from utils.DBHandler import DBHandler

app = Flask(__name__, static_folder="static")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "this_is_a_server_secret_key"

Session(app)

@app.route("/")
def server():
    if not session.get("token"):
        return redirect("/login")
    return redirect("/dashboard")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("token")
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if not session.get("token"):
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    if request.method == "POST":
        user = DBHandler.record("SELECT * FROM Users WHERE Email = ?", request.form.get('email'))
        if user and sha256(request.form.get('password').encode('utf-8')).hexdigest() == user.get("Password"):
            token = sha256(f"{request.form.get('email')}{request.form.get('password')}".encode('utf-8')).hexdigest()
            session["token"] = token
            return make_response(jsonify(token=token), 200)
        return make_response(jsonify(error="Credentials incorrect"), 401)

if __name__ == "__main__":
    with open("src/config.json", 'r') as conf:
        CONFIG = json.loads(conf.read())
    app.run(host=CONFIG.get("HOST"), port=CONFIG.get("PORT"), debug=True)