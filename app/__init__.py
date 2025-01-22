from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import config
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate() 

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "https://bms-api-27l2.onrender.com", "http://localhost:5173","http://bms-api-m3oi.onrender.com",    # Añade esta línea
            "https://bms-api-m3oi.onrender.com" ],  # Añade aquí la URL de tu frontend si es diferente
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    print(f"Current config: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Importar blueprints
        from .routes.buildings import buildings_bp
        from .routes.systems import systems_bp
        from .routes.data import data_bp
        from .routes.commands import commands_bp
        from .routes.signals import signals_bp
        from .routes.modes import modes_bp
        # Registrar blueprints
        app.register_blueprint(buildings_bp)
        app.register_blueprint(systems_bp)
        app.register_blueprint(data_bp)
        app.register_blueprint(commands_bp)
        app.register_blueprint(signals_bp)
        app.register_blueprint(modes_bp)

        # Crear las tablas
        db.create_all()

        print("Registered blueprints:")
        for rule in app.url_map.iter_rules():
            print(f"{rule}")

    return app