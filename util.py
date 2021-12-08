import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import date
from flask import jsonify
from pathlib import Path
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
from psycopg2.extensions import register_adapter, AsIs

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


# def parse_float(numpy_float32):
#     return register_adapter(numpy.float32,AsIs(numpy_float64))
# # register_adapter(numpy.float64, addapt_numpy_float64)
# # register_adapter(numpy.int64, addapt_numpy_int64)

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

def add_song(user, filename, top_classification, tempo, length, classification_arr):
    #  assuming user is present in table
    # try:
        confidence = max(classification_arr, key = lambda i : i[1])[1]
        print(confidence,classification_arr[0][1])

        songs = Table("songs", metadata, autoload=True)
        db.execute(
            songs.insert(),
            userid=get_userid(user),
            filename=filename,
            username=user,
            top_classification=top_classification.capitalize(),
            confidence=round(confidence,5),
            blues=round(classification_arr[0][1],5), 
            classical=round(classification_arr[1][1],5), 
            country=round(classification_arr[2][1],5), 
            disco=round(classification_arr[3][1],5), 
            hiphop=round(classification_arr[4][1],5),
            jazz=round(classification_arr[5][1],5),
            metal=round(classification_arr[6][1],5),
            pop=round(classification_arr[7][1],5),
            reggae=round(classification_arr[8][1],5),
            rock=round(classification_arr[9][1],5),
            tempo = tempo,
            length = length,
            date=str(date.today()),
        )
    #     return True
    # except:
    #     return False

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

def generate_confidence_chart(confidenceArray, file_path):
    plt.close()
    file_name = file_path.split('/')[-1]
    file_type = file_name.split('.')[1]
    song_name = file_name.split('.')[0]
    file_parent_path = Path('/'.join(file_path.split('/')[:-1]))

    labels = [elem[0].capitalize() for elem in confidenceArray]
    values = [elem[1] for elem in confidenceArray]

    colors = ['#e55039','#009432','#1e3799','#fa983a','#079992','#5758BB']
    explode = [.1 for elem in confidenceArray]
    COLOR = 'white'
    mpl.use('Agg')
    mpl.rcParams['text.color'] = COLOR
    mpl.rcParams['axes.labelcolor'] = COLOR
    mpl.rcParams['xtick.color'] = COLOR
    mpl.rcParams['ytick.color'] = COLOR
    mpl.rcParams['font.size'] = 20
    mpl.rcParams["font.family"] = "Arial"
    fig1, ax1 = plt.subplots()
    ax1.pie(values, colors=colors, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=0)
    fig1.set_facecolor((.2,.2,.2))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.      
    plt.savefig(file_parent_path / f"{song_name}-chart.png", dpi=300)