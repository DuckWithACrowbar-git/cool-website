from flask import Flask, render_template, jsonify, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random as r

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per second"],
    storage_uri="memory://",
)


@app.route("/")
def root():
    result_color = ["#"]
    for i in range(6):
        for j in range(3):
            choice = r.choice(values)
        result_color.append(choice)
    result_color = "".join(result_color)
    return render_template('index.html', color=result_color), 200

@app.errorhandler(404)
def page_not_found(error):
    return redirect("/"), 308

@app.errorhandler(429)
def ratelimit_handler(e):
    return "Rate limit exceeded. Slow down."


if __name__ == "__main__":
    app.run(debug=True)