import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
from werkzeug.utils import secure_filename
from pathlib import Path


#this is a really bad way to do this lol
auth_manager = SpotifyClientCredentials(
    client_id='34e24702186c4c24821229b7d080ddae',
    client_secret='4433721d51c64cb782c59bdbcada0f4f'
)
sp = spotipy.Spotify(auth_manager=auth_manager)

def search_album(album):
    return sp.search(q='album:' + album, type='album', limit=25).get('albums').get('items')

def get_playlist(playlist_id):  
    return sp.playlist(playlist_id=playlist_id)

def fetch_user_playlists(user):
    return sp.user_playlists(user).get('items')

def get_playlist(playlist_id):  
    return sp.playlist(playlist_id=playlist_id)

def search_song(track):
    tracks = sp.search(q='track:' + track, type='track', limit=25)
    return tracks.get('tracks').get('items')

def get_track(track_id):
    return sp.track(track_id=track_id)

def download_song(track):
    filename = secure_filename(track.get('name').replace(' ','_') + ".mp3")
    file_path = os.path.join('static/queries/' + filename + '/', filename)
    Path('./static/queries/' + filename).mkdir(parents=True, exist_ok=True)

    r = requests.get(track.get('preview_url'))
    assert r.headers["Content-Type"] == "audio/mpeg"
    f = open(file_path, 'wb')
    f.write(r.content)
    f.close()
    return file_path

# print(search_album("Kauai"))
#download_track(get_track('1nRTH500HbZX8PYwT4ZMby'))