from flask import Flask, render_template, request, url_for
import joblib
import random
import os

app = Flask(__name__)

# Load the trained model and label encoder
model = joblib.load("mood_model.pkl")
le = joblib.load("label_encoder.pkl")

# Predefined song database
song_db = {
    'Happy': [
        {'name': 'Yaarian(ABCD)', 'artist': 'Yo Yo Honey Singh', 'img': 'happy1.jpg', 'file': 'happy1.mp3'},
        {'name': 'Tere Te', 'artist': 'Guru Randhawa', 'img': 'happy2.jpg', 'file': 'happy2.mp3'},
        {'name': 'Jatt Diyan Tauran', 'artist': 'Gippy Grewal, Shipra Goyal', 'img': 'happy3.jpg', 'file': 'happy3.mp3'},
        {'name': 'Jeene Ke Hain Char Din', 'artist': 'Sonu Nigam, Sunidhi Chauhan', 'img': 'happy4.jpg', 'file': 'happy4.mp3'},
        {'name': 'Supreme', 'artist': 'Shubh', 'img': 'happy5.jpg', 'file': 'happy5.mp3'},
        {'name': 'Be Mine', 'artist': 'Shubh', 'img': 'happy6.jpg', 'file': 'happy6.mp3'}
    ],
    'Sad': [
        {'name': 'Kabhi Sham Dhale', 'artist': 'Mohammad Faiz', 'img': 'sad1.jpg', 'file': 'sad1.mp3'},
        {'name': 'Nira Ishq', 'artist': 'Guri', 'img': 'sad2.jpg', 'file': 'sad2.mp3'},
        {'name': 'Pal Pal Dil Ke Pass', 'artist': 'Arijit Singh', 'img': 'sad3.jpg', 'file': 'sad3.mp3'},
        {'name': 'Pal', 'artist': 'Arijit Singh, Javed Mohsin', 'img': 'sad4.jpg', 'file': 'sad4.mp3'},
        {'name': 'Tum Hi Ho', 'artist': 'Mithoon, Arijit Singh', 'img': 'sad5.jpg', 'file': 'sad5.mp3'},
        {'name': 'Tera Hone Laga Hoon', 'artist': 'Atif Aslam, Alisha Chinai', 'img': 'sad6.jpg', 'file': 'sad6.mp3'}
    ],
    'Motivational': [
        {'name': '52 Bars', 'artist': 'Karan Aujla', 'img': 'mot1.jpg', 'file': 'mot1.mp3'},
        {'name': 'Father Saab', 'artist': 'Khasa Aala Chahar', 'img': 'mot2.jpg', 'file': 'mot2.mp3'},
        {'name': 'Game', 'artist': 'Shooter Kahlon, Sidhu Moosewala', 'img': 'mot3.jpg', 'file': 'mot3.mp3'},
        {'name': 'Get Ready To Fight', 'artist': 'Benny Dayal', 'img': 'mot4.jpg', 'file': 'mot4.mp3'},
        {'name': 'Winning Speech', 'artist': 'Karan Aujla', 'img': 'mot5.jpg', 'file': 'mot5.mp3'},
        {'name': 'Aarambh Hai Prachand', 'artist': 'K.K Menon, Abhimannyu Singh', 'img': 'mot6.jpg', 'file': 'mot6.mp3'}
    ],
    'Party': [
        {'name': 'Abhi Toh Party Shuru Hui Hai', 'artist': 'Badshah, Aastha Gill', 'img': 'party1.jpg', 'file': 'party1.mp3'},
        {'name': '5 Taara', 'artist': 'Diljit Dosanjh, Jatinder Shah', 'img': 'party2.jpg', 'file': 'party2.mp3'},
        {'name': 'Daaru Party', 'artist': 'Millind Gaba', 'img': 'party3.jpg', 'file': 'party3.mp3'},
        {'name': 'Party All Night', 'artist': 'Yo Yo Honey Singh', 'img': 'party4.jpg', 'file': 'party4.mp3'},
        {'name': 'Kala Chashma', 'artist': 'Prem Hardeep, Badshah, Neha Kakkar', 'img': 'party5.jpg', 'file': 'party5.mp3'},
        {'name': 'Tujhe Aksa Beech Ghuma Doon', 'artist': 'Wajid, Amrita KaK', 'img': 'party6.jpg', 'file': 'party6.mp3'}
    ]
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            energy = float(request.form['energy'])
            dance = float(request.form['danceability'])
            valence = float(request.form['valence'])

            prediction = model.predict([[energy, dance, valence]])[0]
            mood = le.inverse_transform([prediction])[0]  # Convert label index to label name

            songs = random.sample(song_db[mood], min(6, len(song_db[mood])))

            # Process songs to include proper URLs for images and audio files
            for song in songs:
                song['image_url'] = url_for('static', filename=f'images/{song["img"]}')
                song['audio_url'] = url_for('static', filename=f'audio/{song["file"]}')

            return render_template("index.html", mood=mood, songs=songs)
        except Exception as e:
            return f"Error occurred: {e}"

    return render_template("index.html", mood=None)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, url_for
import joblib
import random
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# === ENTER YOUR SPOTIFY CREDENTIALS HERE ===
SPOTIFY_CLIENT_ID = "31cce518dbd942978bedb5acf0392969"
SPOTIFY_CLIENT_SECRET = "1a44238b864842c78b3ee4bac71bd50a"

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET))

# Load the trained model and label encoder
model = joblib.load("mood_model.pkl")
le = joblib.load("label_encoder.pkl")

def fetch_spotify_tracks(mood):
    try:
        results = sp.search(q=f"{mood} bollywood", type='track', limit=6)
        songs = []
        for item in results['tracks']['items']:
            song = {
                'name': item['name'],
                'artist': ', '.join(artist['name'] for artist in item['artists']),
                'image_url': item['album']['images'][0]['url'] if item['album']['images'] else "",
                'audio_url': item['preview_url']  # 30-second preview
            }
            songs.append(song)
        return songs
    except Exception as e:
        print(f"Spotify API error: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            energy = float(request.form['energy'])
            dance = float(request.form['danceability'])
            valence = float(request.form['valence'])

            prediction = model.predict([[energy, dance, valence]])[0]
            mood = le.inverse_transform([prediction])[0]

            songs = fetch_spotify_tracks(mood)

            return render_template("index.html", mood=mood, songs=songs)
        except Exception as e:
            return f"Error occurred: {e}"

    return render_template("index.html", mood=None)


