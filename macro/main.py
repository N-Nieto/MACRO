"""Initiate the application."""


from flask import Flask
from flask_session import Session


# from .config import Config

# Initiate Flask application
app = Flask(__name__)

# Load configuration
app.config.from_pyfile("config_dev.py")

# Setup Flask-Session
Session(app)

# Import routing to render the pages
from .views import *
