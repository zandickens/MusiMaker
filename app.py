from fileinput import filename
import flask
import json
import os
import base64
import sys
from pathlib import Path
from flask import Flask, redirect, request, make_response, flash, url_for, Response
from flask.templating import render_template
from util import add_song, create_user, sign_in_user, get_all_songs, get_user_songs, get_song, generate_data
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.utils import secure_filename
from Backend.spectrogramgenerator import generate_spectrogram
from Backend.queryflask import load_latest_model
from Backend.spotify import get_track,download_song,search_song, search_album, fetch_user_playlists, download_song
from Backend.MusicGenerator import generateDrums, generateMelody

EXTENSIONS = {'wav','mp3','mid'}

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = True
app.secret_key = os.urandom(24)
prediction_model = load_latest_model()

global user
user = "no_current_user"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSIONS

def set_user(username):
    global user
    user = username


@app.route("/")
def homepage():
    return flask.render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    return flask.render_template("login.html")


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

@app.route("/sign_out", methods=["GET", "POST"])
def sign_out():
        set_user("no_current_user")
        return flask.redirect("http://localhost:5000/")


@app.route("/upload_song", methods=["POST", "GET"])
def upload_song():
    # need to get filename, classification, and confidence level from backend ssadas
    global user
    if user == "no_current_user":
        flash ("NOT SIGNED IN")
        return flask.redirect("http://localhost:5000/")
    if request.method == "POST":
        if 'file' not in request.files:
            print('File not found', flush=True)
            return redirect("http://localhost:5000/")
        file = request.files['file']
        if file.filename == '':
            print('No selected file', flush=True)
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/queries/' + filename + '/', filename)
            Path('static/queries/' + filename).mkdir(parents=True, exist_ok=True)
            file.save(file_path)
            file.close()
            print('File saved to disk.')
            generate_data( prediction_model=prediction_model, file_path=file_path, filename=filename, user=user)
            return flask.redirect(url_for('get_song_results',username=user, filename=filename))

@app.route("/global_uploads")
def song_results():
    songs = get_all_songs()
    return flask.render_template("global_uploads.html", user=user, songs=songs)

@app.route("/user_uploads", methods=["POST", "GET"])
def get_user_page():
    if user == "no_current_user":
        return flask.redirect("http://localhost:5000")
    return flask.redirect(url_for('get_user_uploads',username=user))

@app.route("/user_uploads/<username>", methods=["POST", "GET"])
def get_user_uploads(username):
    songs = get_user_songs(username)
    global user
    return flask.render_template("user_uploads.html", user=user, username=username,songs=songs)

@app.route("/song_results/<username>/<filename>", methods=["POST", "GET"])
def get_song_results(username, filename):
    songname = filename.split('.')[0]
    chartFilename =  f"{songname}-chart.png"
    spectrogramFilename = f"{songname}-spectrogram.png"
    song = get_song(username,filename)
    return flask.render_template("song_results.html",user=user, username=username, filename=filename, song=song, chartFilename=chartFilename, spectrogramFilename = spectrogramFilename)

@app.route('/spotify_search', methods=["POST", "GET"])
def spotify():
    return flask.render_template('spotify_search.html',user=user)
     
@app.route('/spotify_song', methods=["POST", "GET"])
def spotify_song():
    song = request.args.get('spsearch')
    spotify_songs = search_song(song)
    return flask.render_template('spotify_song_search.html',user=user, songs=spotify_songs)

@app.route('/spotify_album', methods=["POST", "GET"])
def spotify_album():
    album = request.args.get('spsearch')
    albums = search_album(album)
    return flask.render_template('spotify_album_search.html',user=user, albums=albums)

@app.route('/spotify_playlist', methods=["POST", "GET"])
def spotify_playlist():
    spotify_user = request.args.get('spsearch')
    playlists = fetch_user_playlists(spotify_user)
    return flask.render_template('spotify_playlist_search.html',user=user, playlists=playlists)

@app.route('/spotify_song/<track_id>', methods=["POST", "GET"])
def upload_spotify_song(track_id):
    track = get_track(track_id=track_id)
    file_path = download_song(track)
    filename = os.path.basename(file_path)
    generate_data(prediction_model=prediction_model,file_path=file_path, filename=filename, user=user)
    return flask.redirect(url_for('get_song_results',username=user, filename=filename))

@app.route('/midi_upload', methods=["POST", "GET"])
def midi_upload():
    return flask.render_template('midi_upload.html',user=user)

@app.route('/midi_melody_upload', methods=["POST", "GET"])
def midi_melody_upload():
    filename = ''
    if request.method == "POST":
        if 'file' not in request.files:
            print('File not found', flush=True)
            return redirect("http://localhost:5000/not_in")
        file = request.files['file']
        if file.filename == '':
            print('No selected file', flush=True)
            return redirect("http://localhost:5000/no_selected")
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = 'static/queries/midi_temp_upload/temp.mid'
            file.save(file_path)
            file.close()
            print('File saved to disk.')
            generateMelody(file.filename)

    return flask.redirect('/midi_results/'+filename)

@app.route('/midi_drum_upload', methods=["POST", "GET"])
def midi_drum_upload():
    filename = ''
    if 'file' not in request.files:
        print('File not found', flush=True)
        return redirect("http://localhost:5000/not_in")
    file = request.files['file']
    if file.filename == '':
        print('No selected file', flush=True)
        return redirect("http://localhost:5000/no_selected")
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = 'static/queries/midi_temp_upload/temp.mid'
        file.save(file_path)
        file.close()
        print('File saved to disk.')
        generateDrums(file.filename)

    return flask.redirect('/midi_results/'+file.filename)

@app.route('/midi_results/<recent_file>', methods=["POST", "GET"])
def midi_results(recent_file):
    return flask.render_template('midi_results.html',user=user,recent_file=recent_file)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
 