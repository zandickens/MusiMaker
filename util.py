import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
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
    top_classification = Column(String)
    confidence = Column(Float)
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
    tempo = Column(Float)
    length = Column(Float)
    tempo = Column(Float)
    length = Column(Float)
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

def add_song(user, filename, top_classification, confidence, tempo, length, blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock):
    #  assuming user is present in table
    try:
        songs = Table("songs", metadata, autoload=True)
        db.execute(
            songs.insert(),
            userid=get_userid(user),
            filename=filename,
            username=user,
            top_classification=top_classification,
            confidence=confidence,
            blues=blues, 
            classical=classical, 
            country=country, 
            disco=disco, 
            hiphop=hiphop,
            jazz=jazz,
            metal=metal,
            pop=pop,
            reggae=reggae,
            rock=rock,
            tempo = tempo,
            length = length,
            date=datetime.now(),
        )
        return True
    except:
        return False

def delete_song(user, filename):
    try:
        songs =session.query(Songs).join(Users, Users.userid==Songs.userid).filter(Users.username == username).filter( Songs.userid == Users.userid ).filter( Songs.filename == filename).delete()
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
            'top_classification' : song.top_classification,
            'confidence' : song.confidence,
            'blues' : song.blues, 
            'classical' : song.classical, 
            'country' : song.country, 
            'disco' : song.disco, 
            'hiphop' : song.hiphop,
            'jazz' : song.jazz,
            'metal' : song.metal,
            'pop' : song.pop,
            'reggae' : song.reggae,
            'rock' : song.rock,
            'tempo' : song.tempo,
            'length' : song.length,
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
            'top_classification' : song.top_classification,
            'confidence' : song.confidence,
            'blues' : song.blues, 
            'classical' : song.classical, 
            'country' : song.country, 
            'disco' : song.disco, 
            'hiphop' : song.hiphop,
            'jazz' : song.jazz,
            'metal' : song.metal,
            'pop' : song.pop,
            'reggae' : song.reggae,
            'rock' : song.rock,
            'tempo' : song.tempo,
            'length' : song.length,
            'date' : song.date.strftime('%m-%d-%Y')
        })
    return song_arr

def get_song(username,filename):
    songs =session.query(Songs).join(Users, Users.userid==Songs.userid).filter(Users.username == username).filter( Songs.userid == Users.userid ).filter( Songs.filename == filename).all()
    song = {
        'song_id' : songs[0].songid,
        'user_id' : songs[0].userid,
        'user_name' : songs[0].username,
        'filename' : songs[0].filename,
        'top_classification' : songs[0].top_classification,
        'confidence' : songs[0].confidence,
        'blues' : songs[0].blues, 
        'classical' : songs[0].classical, 
        'country' : songs[0].country, 
        'disco' : songs[0].disco, 
        'hiphop' : songs[0].hiphop,
        'jazz' : songs[0].jazz,
        'metal' : songs[0].metal,
        'pop' : songs[0].pop,
        'reggae' : songs[0].reggae,
        'rock' : songs[0].rock,
        'tempo' : songs[0].tempo,
        'length' : songs[0].length,
        'date' : songs[0].date
    }
    return song

def generate_confidence_chart(confidenceArray, filename):
    labels = [elem[0].upper() for elem in confidenceArray]
    values = [elem[1] for elem in confidenceArray]
    colors = ['#ff6b81','#5352ed','#eccc68','#ff7f50','#7bed9f','#57606f']
    explode = (.1,.1,.1,.1,.1,.1,.1,.1,.1,.1)
    COLOR = 'white'
    mpl.rcParams['text.color'] = COLOR
    mpl.rcParams['axes.labelcolor'] = COLOR
    mpl.rcParams['xtick.color'] = COLOR
    mpl.rcParams['ytick.color'] = COLOR
    fig1, ax1 = plt.subplots()
    ax1.pie(values, colors=colors, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0)
    fig1.set_facecolor((.2,.2,.2))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.      

    plt.savefig("static/queries/" + filename + "/" + filename + "_chart.png", dpi=300)