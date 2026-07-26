from flask import Flask, render_template, jsonify, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from time import sleep
import threading as t
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

URL = "https://api.weather.gov/alerts/active/area/TX"
TIME_TO_WAIT = 5 * 60
alert_id = None
sent_date = None
expiry_date = None
severity = None
certainty = None
description = None
instruction = None

def get_data():
    while True:
        response = requests.get(URL)
        data = response.json()
        global alert_id, sent_date, expiry_date, severity, certainty, description, instruction
        alert_id = (data["features"][0]["properties"]["@id"])
        sent_date = (data["features"][0]["properties"]["sent"])
        expiry_date = (data["features"][0]["properties"]["expires"])
        severity = (data["features"][0]["properties"]["severity"])
        certainty = (data["features"][0]["properties"]["certainty"])
        description = (data["features"][0]["properties"]["description"])
        instruction = (data["features"][0]["properties"]["instruction"])
        sleep(TIME_TO_WAIT)


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60/minute"],
    storage_uri="memory://",
)

@app.route("/")
def root():
    return render_template('index.html', 
                           alert_id=alert_id, 
                           sent_date=sent_date, 
                           expiry_date=expiry_date, 
                           severity=severity,
                           certainty=certainty,
                           description=description,
                           instruction=instruction), 200

if __name__ == "__main__":
    thread = t.Thread(target=get_data, daemon=True)
    thread.start()
    app.run()