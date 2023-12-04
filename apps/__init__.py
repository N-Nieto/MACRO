# -*- encoding: utf-8 -*-
import os

# import Flask
from flask import Flask
from flask_session import Session

from .config import Config

# Inject Flask magic
app = Flask(__name__)

# load Configuration
app.config.from_object(Config)
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
# Import routing to render the pages
from apps import views