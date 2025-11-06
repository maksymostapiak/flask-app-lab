from flask import Flask
from app.users.views import users_bp 
from app.products.views import products_bp

app = Flask(__name__)
app.config.from_pyfile("../config.py")
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.secret_key = "flassecretkey"

from app import views