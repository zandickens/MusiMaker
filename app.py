import flask
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, request, make_response,jsonify
from sqlalchemy import create_engine, Table, MetaData, Table, Column, Integer, String, Date, ForeignKey, Sequence, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, func
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(24)

db = create_engine(os.environ['DB_URL'])
metadata = MetaData(db)

ORM_Base = declarative_base()

class Users(ORM_Base):
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    creation_date = Column(Date)

class Songs(ORM_Base):
    __tablename__ = 'songs'
    songId = Column(Integer, primary_key=True)
    userId = Column(Integer)
    filename =Column(String)
    blues = Column(Float) 
    classical = Column(Float) 
    country = Column(Float) 
    disco = Column(Float) 
    hiphop = Column(Float) 
    jazz = Column(Float) 
    metal = Column(Float) 
    pop = Column(Float) 
    reggae = Column(Float) 
    rock = Column(Float)
    date = Column(Date)

Session = sessionmaker(bind=db)
session = Session()

@app.route('/')
def homepage():
    return flask.render_template('index.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    return 'file uploaded successfully'

@app.route('/register', methods=["GET", "POST"])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    password_hash = generate_password_hash(password)
    users = Table('users', metadata, autoload=True)
    db.execute(users.insert(), username=username,
                   password=password_hash, )
    return jsonify({'user_added': True})

@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    username_entered = request.args.get('username')
    password_entered = request.args.get('password')
    user = session.query(Users).filter(
        Users.username == username_entered, 
    ).first()
    if user is not None and check_password_hash(user.password, password_entered):
        return jsonify({'signed_in': True})
    return jsonify({'signed_in': False})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)