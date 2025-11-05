from flask import Flask
from app.users.views import users_bp 

app = Flask(__name__)
app.config.from_pyfile("../config.py")
app.register_blueprint(users_bp)

from app import views