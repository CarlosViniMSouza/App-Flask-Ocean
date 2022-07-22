from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

flask_app = os.getenv("FLASK_APP")
flask_env = os.getenv("FLASK_ENV")

app = Flask(__name__)


@app.route("/")
def root():
    return "<h1> Hello, Flask! </h1>"
