![MusiMaker Logo](https://github.com/zandickens/MusiMaker/blob/main/static/assets/images/logo.png)

# MusiMaker

- 

## About
MusiMaker is a software designed to classify audio files by numerous parameters and create a beat similar to songs given by the user. The software will take in any audio file (.mp4, .wav, ect.) and generate a MIDI file with a beat similar to inputted songs.
When creating a new beat/song, many people have samples that they want their new beat to sound similar to. With MusiMaker, this user would be able to create a template beat directly from a list of songs they choose. This app would also allow for organization and storage of the user's favorite generated samples, as well as songs they like to use when generating new music.
This application would be useful for those skilled at making music to generate a template beat that can be tweaked to their exact specification at a later time. It is also useful for those just starting making music as it provides an easy way to make a beat with little to no previous experience. Lastly, it is fun to be able to hear mashups of some of your favorite songs!

## Setup

To run MusiMaker, Flask must be installed locally. First, create a virtual environment in the root of the project directory.

``` python3 -m venv venv ```

On a UNIX based operating system, to operate within the virtual environment, run this command:

``` source venv/bin/activate ```

On Windows, this command will do:

``` venv/Scripts/activate ```

Once the (venv) is running, install Flask with the following command.

``` (venv) $ pip3 install flask ``` 

That's it! Now just run the MusiMaker web app with

``` python3 app.py ```
