from markupsafe import escape
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        "title": "First Post",
        "body": "Text of false post :)",
        "author": "CarlosViniMSouza",
        "created": datetime(2022, 7, 26)
    },
    {
        "title": "Second Post",
        "body": "Text of second false post :|",
        "author": "CVMDS",
        "created": datetime(2022, 7, 25)
    },
    {
        "title": "Third Post",
        "body": "Text of last false post! u.u",
        "author": "CarloSouza",
        "created": datetime(2022, 7, 24)
    }
]


@app.route("/")
def root():
    return "<h1> Hello, Flask! </h1>"


@app.route("/contacts")
def contacts():
    name = "Carlos Souza"
    username = "@CarlosViniMSouza"
    email = "vinicius.souza@gmail.com"

    return render_template("index.html", name=name, username=username, email=email, posts=posts)
