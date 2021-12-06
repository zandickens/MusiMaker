import flask
import json
import os
from flask import Flask, redirect, request, make_response, flash
from flask.templating import render_template
from util import add_song, create_user, sign_in_user
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = True
app.secret_key = os.urandom(24)

global user
user = "no_current_user"


def set_user(username):
    global user
    user = username


@app.route("/")
def homepage():
    return flask.render_template("index.html", user=user)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    return "file uploaded successfully"


@app.route("/login", methods=["GET", "POST"])
def login_page():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    username_entered = request.args.get("uname")
    password_entered = request.args.get("psw")
    if create_user(username_entered, password_entered):
        set_user(username_entered)
        return flask.redirect("http://localhost:5000/")
    return flask.redirect("http://localhost:5000/login")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    username_entered = request.args.get("uname")
    password_entered = request.args.get("psw")
    if sign_in_user(username_entered, password_entered):
        set_user(username_entered)
        return flask.redirect("http://localhost:5000/")
    return flask.redirect("http://localhost:5000/login")


@app.route("/upload_song", methods=["POST", "GET"])
def upload_song():
    # need to get filename, classification, and confidence level from backend ssadas
    global user
    # file = request
    body = request.get_data("body")
    print("\n\n" + str(request.get_data("name")))
    # classification = "metal"
    # confidence = 0.99
    # if add_song(user, filename, classification, confidence):
    #     return flask.redirect("http://localhost:5000/")
    # print("error adding song")
    return flask.redirect("http://localhost:5000/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
