from flask import Flask, render_template, jsonify, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random as r

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60/minute"],
    storage_uri="memory://",
)

playlist = [
    {"title": "Never Gonna Give You Up", "file": "rickroll.mp3", "author": "Rick Astley"},
    {"title": "Billie Jean", "file": "billie_jean.mp3", "author": "Micheal Jackson"},
    {"title": "Sweet Child O' Mine", "file": "sweet_child.mp3", "author": "Guns N' Roses"},
    {"title": "Smells Like Teen Spirit", "file": "teen_spirit.mp3", "author": "Nirvana"},
    {"title": "Wonderwall", "file": "wonderwall.mp3", "author": "Oasis"},
    {"title": "Crazy In Love", "file": "crazy_in_love.mp3", "author": "Beyoncé"},
    {"title": "Bad Romance", "file": "bad_romance.mp3", "author": "Lady Gaga"},
    {"title": "Like A Prayer", "file": "like_a_prayer.mp3", "author": "Madonna"},
    {"title": "With Or Without You", "file": "with_or_without_you.mp3", "author": "U2"},
    {"title": "Every Breath You Take", "file": "every_breath_you_take.mp3", "author": "The Police"},
    {"title": "No Scrubs", "file": "no_scrubs.mp3", "author": "TLC"},
    {"title": "I Want It That Way", "file": "that_way.mp3", "author": "Backstreet Boys"},
    {"title": "In The End", "file": "in_the_end.mp3", "author": "Linkin Park"},
    {"title": "Crazy", "file": "crazy.mp3", "author": "Gnarls Barkley"},
    {"title": "Umbrella", "file": "umbrella.mp3", "author": "Rihanna"},
    {"title": "Viva La Vida", "file": "vlv.mp3", "author": "Coldplay"},
    {"title": "Poker Face", "file": "poker_face.mp3", "author": "Lady Fafa"},
]

@app.route("/")
def root():
    for i in range(10):
        song = r.choice(playlist)
    return render_template('index.html', song=song), 200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('ratelimit.html'), 200


if __name__ == "__main__":
    app.run(debug=True)