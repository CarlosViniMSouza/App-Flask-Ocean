from flask import Flask, render_template, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(70), nullable=False)
    body = db.Column(db.String(500))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False,
                         unique=True, index=True)
    email = db.Column(db.String(64), nullable=False,
                      unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref="author")


db.create_all()


@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/populate")
def populate():
    user = User(
        username="Carlos", 
        email="@gmail.com", 
        password_hash='crypto'
    )

    post1 = Post(
        title="Fake Text 01",
        body="Created a fake text for test",
        author="CarlosViniMSouza"
    )

    post2 = Post(
        title="Fake Text 02",
        body="Created a fake text for test",
        author="CarloSouza"
    )

    db.session.add(user)
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

    return redirect(url_for('index'))
