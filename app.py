import flask
import json
import os
from flask import Flask, redirect, request, make_response
from util import create_user, sign_in_user
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(24)

@app.route('/')
def homepage():
    return flask.render_template('index.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    return 'file uploaded successfully'

@app.route('/register', methods=["GET", "POST"])
def register():
    username_entered = request.args.get('username')
    password_entered = request.args.get('password')
    return create_user(username_entered,password_entered)

@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    username_entered = request.args.get('username')
    password_entered = request.args.get('password')
    return sign_in_user(username_entered,password_entered)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)