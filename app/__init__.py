from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
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
