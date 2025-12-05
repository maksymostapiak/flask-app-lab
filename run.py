import os
from app import create_app
from config import DevelopmentConfig, TestingConfig, ProductionConfig

config_modes = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

mode = os.getenv("FLASK_CONFIG", "development")

app = create_app(config_modes[mode])

if __name__ == "__main__":
    app.run(debug=True)
