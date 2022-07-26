from markupsafe import escape
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def root():
    return "<h1> Hello, Flask! </h1>"


@app.route("/contacts")
def contacts():
    name = "Carlos Souza"
    username = "@CarlosViniMSouza"
    email = "vinicius.souza@gmail.com"

    return render_template("index.html", name=name, username=username, email=email)
