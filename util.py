import os
from datetime import date
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Sequence,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, func
from sqlalchemy.orm import sessionmaker, relationship

db = create_engine(os.environ["DB_URL"])
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

ORM_Base = declarative_base()


class Users(ORM_Base):
    __tablename__ = "users"
    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    creation_date = Column(Date)


class Songs(ORM_Base):
    __tablename__ = "songs"
    songid = Column(Integer, primary_key=True)
    userid = Column(Integer)
    username = Column(String)
    filename = Column(String)
    classification = Column(String)
    confidence = Column(Float)
    date = Column(Date)


def create_user(username, password):
    try:
        password_hash = generate_password_hash(password)
        users = Table("users", metadata, autoload=True)
        db.execute(
            users.insert(),
            username=username,
            password=password_hash,
        )
        return True
    except:
        return False


def sign_in_user(username, password):
    user = (
        session.query(Users)
        .filter(
            Users.username == username,
        )
        .first()
    )
    if user is not None:
        return check_password_hash(user.password, password)
    return False


def get_userid(username):
    user = (
        session.query(Users)
        .filter(
            Users.username == username,
        )
        .first()
    )
    return user.userid

def add_song(user, filename, classification, confidence):
    #  assuming user is present in table
    try:
        songs = Table("songs", metadata, autoload=True)
        db.execute(
            songs.insert(),
            userid=get_userid(user),
            filename=filename,
            username=user,
            classification=classification,
            confidence=confidence,
            date=date.today(),
        )
        return True
    except:
        return False

def get_all_songs():
    songs = session.query(Songs).all()
    # for song in songs:
    # for i in range(0,10):
    # add_song('aidan', 'test'+str(i),'test',0.0)
    song_arr = []
    for song in songs:
        song_arr.append({
            'song_id' : song.songid,
            'user_id' : song.userid,
            'user_name' : song.username,
            'filename' : song.filename,
            'classification' : song.classification,
            'confidence' : song.confidence,
            'date' : song.date.strftime('%m-%d-%Y')
        })
    return song_arr

def get_user_songs(username):
    songs = session.query(Songs).join(Users, Users.userid==Songs.userid).filter(Users.username == username).filter( Songs.userid == Users.userid ).all()
    song_arr = []
    for song in songs:
        song_arr.append({
            'song_id' : song.songid,
            'user_id' : song.userid,
            'user_name' : song.username,
            'filename' : song.filename,
            'classification' : song.classification,
            'confidence' : song.confidence,
            'date' : song.date.strftime('%m-%d-%Y')
        })
    return song_arr

def get_song(filename):
    songs = (
        session.query(Songs)
        .filter(
            Songs.filename == filename,
        )
    )