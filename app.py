from flask import Flask, render_template, jsonify, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from time import sleep, ctime
import threading as t
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

URL = "https://api.weather.gov/alerts/active/area/TX"
TIME_TO_WAIT = 60
alert_id = " "
sent_date = " "
expiry_date = " "
severity = " "
certainty = " "
event = " "
description = " "
instruction = " "
NWSheadline = " "

def get_data():
    sleep(5)
    while True:
        response = requests.get(URL)
        data = response.json()
        global alert_id, sent_date, expiry_date, severity, certainty, event, description, instruction, NWSheadline
        alert_id = (data["features"][0]["properties"]["@id"])
        sent_date = (data["features"][0]["properties"]["sent"])
        expiry_date = (data["features"][0]["properties"]["expires"])
        severity = (data["features"][0]["properties"]["severity"])
        certainty = (data["features"][0]["properties"]["certainty"])
        event = (data["features"][0]["properties"]["event"])
        description = (data["features"][0]["properties"]["description"])
        instruction = (data["features"][0]["properties"]["instruction"])
        NWSheadline = (data["features"][0]["properties"]["parameters"]["NWSheadline"][0])
        print("Pulled data at " + ctime())
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
                           event=event,
                           desc=description,
                           instruction=instruction,
                           headline=NWSheadline), 200

@app.route("/about")
def about():
    return render_template('about.html'), 200

@app.route("/api")
def api():
    value = jsonify({"alert_id": alert_id, 
                     "sent_date": sent_date, 
                     "expiry_date": expiry_date, 
                     "severity": severity, 
                     "certainty": certainty, 
                     "event": event, 
                     "description": description, 
                     "instruction": instruction,
                     "headline": NWSheadline})
    return value, 200

@app.errorhandler(429)
def ratelimit(error):
    return render_template('ratelimit.html'), 200

@app.errorhandler(404)
def ratelimit(error):
    return render_template('404.html'), 200

if __name__ == "__main__":
    thread = t.Thread(target=get_data, daemon=True)
    thread.start()
    app.run()