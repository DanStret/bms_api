from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import config
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "https://bms-api-27l2.onrender.com"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    print(f"Current config: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    db.init_app(app)
    ma.init_app(app)
    CORS(app)
    
    with app.app_context():
        # Importar blueprints
        from .routes.buildings import buildings_bp
        from .routes.systems import systems_bp
        from .routes.data import data_bp
        from .routes.commands import commands_bp
        from .routes.signals import signals_bp

        # Registrar blueprints
        app.register_blueprint(buildings_bp)
        app.register_blueprint(systems_bp)
        app.register_blueprint(data_bp)
        app.register_blueprint(commands_bp)
        app.register_blueprint(signals_bp)

        # Crear las tablas
        db.create_all()

        print("Registered blueprints:")
        for rule in app.url_map.iter_rules():
            print(f"{rule}")

    return app