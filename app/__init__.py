from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///huntdog.db"
app.config["SECRET_KEY"] = "secret_key_here"

db = SQLAlchemy(app)

from app import routes