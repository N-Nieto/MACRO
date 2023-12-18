"""Production configuration for the Flask application."""""

# Flask
ENV = "production"
DEBUG = False
SECRET_KEY = "c657e0c264605566da2e470e6d2cc599"
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
PERMANENT_SESSION_LIFETIME = 1800
ASSETS_ROOT = "/static/assets"

# Flask-Session
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "./session/"
