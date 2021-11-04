import flask
from flask import Flask, redirect, request, make_response

app = Flask(__name__)

@app.route('/')
def homepage():
    return flask.render_template('index.html')


@app.route('/upload')
def upload():
    return flask.render_template('upload.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)