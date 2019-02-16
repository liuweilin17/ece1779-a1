from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from flaskr import home
from flaskr import login
from flaskr import upload