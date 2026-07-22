from flask import Flask, render_template, jsonify
import random as r
import requests

URL = "http://localhost:5000"

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def root():
    # response = requests.get(URL+"/random").text
    return render_template('index.html')

@app.route("/random", methods=['GET'])
def random():
    for i in range(10):
        rand = r.random()
    rand = str(rand)
    rand = rand.replace("0.", "")
    rand = int(rand)
    return jsonify(rand), 200


if __name__ == "__main__":
    app.run(debug=True)