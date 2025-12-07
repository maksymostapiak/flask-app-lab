from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        from config import DevelopmentConfig
        config_class = DevelopmentConfig

    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    from app.posts.models import Post
    from app.products.models import Product
    from app.users.views import users_bp
    from app.products.views import products_bp
    from app.views import views_bp
    from app.posts.views import posts_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(posts_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app
