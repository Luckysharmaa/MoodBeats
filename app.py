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
        {'name': 'Phir Se Ud Chala', 'img': 'happy1.jpg', 'file': 'happy1.mp3'},
        {'name': 'Iiahi', 'img': 'happy2.jpg', 'file': 'happy2.mp3'},
        {'name': 'Kabira', 'img': 'happy3.jpg', 'file': 'happy3.mp3'},
        {'name': 'Gallan Goodiyaan', 'img': 'happy4.jpg', 'file': 'happy4.mp3'},
        {'name': 'Sheher Mein', 'img': 'happy5.jpg', 'file': 'happy5.mp3'},
        {'name': 'Chiggy Wiggy', 'img': 'happy6.jpg', 'file': 'happy6.mp3'}
    ],
    'Sad': [
        {'name': 'Channa Mereya', 'img': 'sad1.jpg', 'file': 'sad1.mp3'},
        {'name': 'Tadap', 'img': 'sad2.jpg', 'file': 'sad2.mp3'},
        {'name': 'Agar Tum Sath Ho', 'img': 'sad3.jpg', 'file': 'sad3.mp3'},
        {'name': 'Har Ghadi Badal Rahi Hai', 'img': 'sad4.jpg', 'file': 'sad4.mp3'},
        {'name': 'Abhi Na Jao chod ker', 'img': 'sad5.jpg', 'file': 'sad5.mp3'},
        {'name': 'Pal Pal Dil ke Paas', 'img': 'sad6.jpg', 'file': 'sad6.mp3'}
    ],
    'Motivational': [
        {'name': 'Zinda', 'img': 'mot1.jpg', 'file': 'mot1.mp3'},
        {'name': 'Lakshya', 'img': 'mot2.jpg', 'file': 'mot2.mp3'},
        {'name': 'Aashayein', 'img': 'mot3.jpg', 'file': 'mot3.mp3'},
        {'name': 'Kar Har Maidan Fateh', 'img': 'mot4.jpg', 'file': 'mot4.mp3'},
        {'name': 'Sultan', 'img': 'mot5.jpg', 'file': 'mot5.mp3'},
        {'name': 'Dangal', 'img': 'mot6.jpg', 'file': 'mot6.mp3'}        
    ],
    'Party': [
        {'name': 'Kala Chashma', 'img': 'party1.jpg', 'file': 'party1.mp3'},
        {'name': 'Nashe si chadh gayi', 'img': 'party2.jpg', 'file': 'party2.mp3'},
        {'name': 'Lungi Dance', 'img': 'party3.jpg', 'file': 'party3.mp3'},
        {'name': 'Malhari', 'img': 'party4.jpg', 'file': 'party4.mp3'},
        {'name': 'Afghaan Jalebi', 'img': 'party5.jpg', 'file': 'party5.mp3'},
        {'name': 'Aayi Na', 'img': 'party6.jpg', 'file': 'party6.mp3'}
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
