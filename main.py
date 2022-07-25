from markupsafe import escape
from flask import Flask

app = Flask(__name__)


@app.route("/")
def root():
    return "<h1> Hello, Flask! </h1>"


@app.route("/hello/<user>")
def helloUser(user):
    return f"<h2> hello, {escape(user)} </h2>"
