from flask import Flask, render_template, url_for, redirect, request
import requests
from pymarkovchain import MarkovChain
import os

API_KEY = os.environ.get('API_KEY')
PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/lyrics', methods=['POST'])
def lyrics():
    artist = request.form['artist']
    lines = int(request.form['lines'])

    if not artist:
        return redirect(url_for('index'))

    # Get a response of sample lyrics from the provided artist
    uri = "http://api.lyricsnmusic.com/songs"
    params = {
        'api_key': API_KEY,
        'artist': artist,
    }
    response = requests.get(uri, params=params)
    lyric_list = response.json()
    # Parse results into a long string of lyrics
    lyrics = ''
    for lyric_dict in lyric_list:
        lyrics += lyric_dict['snippet'].replace('...', '') + ' '

    # Generate a Markov model
    mc = MarkovChain()
    mc.generateDatabase(lyrics)

    result = []
    for line in range(0, lines):
        result.append(mc.generateString())

    return render_template('lyrics.html', result=result, artist=artist)

if __name__== '__main__':
    app.run(host='0.0.0.0', port=PORT)
