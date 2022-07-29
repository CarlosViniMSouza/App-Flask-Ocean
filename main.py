from datetime import datetime

# database modules
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# login/register/security user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "app-flask-python"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login = LoginManager(app)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(70), nullable=False)
    body = db.Column(db.String(500))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False,
                         unique=True, index=True)
    email = db.Column(db.String(64), nullable=False,
                      unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref="author")

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def loadUser(id):
    return User.query.get(int(id))


db.create_all()


@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route('/register', methods=["GET", "POST"])
def registerUser():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        try:
            newUser = User(
                username=username,
                email=email
            )

            newUser.set_password(password)
            db.session.add(newUser)
            db.session.commit()

        except IntegrityError:
            flash("Username/E-mail already exists!")
        else:
            return redirect(url_for("auth/login"))
    return render_template("auth/register.html")


@app.route("/login", methods=["GET", "POST"])
def loginUser():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user is None or not user.checkPassword(password):
            flash("Username/Password Incorrect!")
            return redirect(url_for("auth/login"))

        login_user(user)
        return redirect(url_for("index"))

    return render_template("auth/login.html")


@app.route("/logout")
def logoutUser():
    logout_user()
    return redirect(url_for("index"))
