import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Assets Management
    ASSETS_ROOT = os.getenv("ASSETS_ROOT", "/static/assets")

    # App Config - the minimal footprint
    SECRET_KEY = os.getenv("SECRET_KEY", "secret#key#2020#")
