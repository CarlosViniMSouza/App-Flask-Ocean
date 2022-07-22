from dotenv import load_dotenv
from markupsafe import escape
from flask import Flask
import os

load_dotenv()

flask_app = os.getenv("FLASK_APP")
flask_env = os.getenv("FLASK_ENV")

app = Flask(__name__)


@app.route("/")
def root():
    return "<h1> Hello, Flask! </h1>"


@app.route("/hello/<user>")
def helloUser(user):
    return f"<h2> hello, {escape(user)} </h2>"

# CRUD -> get() | post() | put() | delete()
