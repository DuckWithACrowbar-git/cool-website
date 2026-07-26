from flask import Flask, render_template, jsonify, redirect, url_for
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

@app.route("/")
def root():
    return render_template('index.html'), 200

if __name__ == "__main__":
    app.run(debug=True)