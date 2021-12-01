import os
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Table, MetaData, Table, Column, Integer, String, Date, ForeignKey, Sequence, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, func
from sqlalchemy.orm import sessionmaker, relationship

db = create_engine(os.environ['DB_URL'])
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

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

def create_user(username,password):
    password_hash = generate_password_hash(password)
    users = Table('users', metadata, autoload=True)
    db.execute(users.insert(), username=username,
                   password=password_hash, )
    return jsonify({'user_added': True})

def sign_in_user(username,password):
    user = session.query(Users).filter(
        Users.username == username, 
    ).first()

    if user is not None and check_password_hash(user.password, password):
        return jsonify({'signed_in': True})
    return jsonify({'signed_in': False})
