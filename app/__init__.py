from flask import Flask, jsonify
from flask_cors import CORS  # Importa CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import config
import pymysql

# Configura pymysql para MySQL
pymysql.install_as_MySQLdb()

# Inicializa las extensiones
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_name='default'):
    # Crea la aplicación Flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configuración de CORS de manera global
    CORS(app)  # Habilita CORS para todas las rutas y orígenes

    # Imprime la configuración actual (para depuración)
    print(f"Current config: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Inicializa las extensiones con la aplicación
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Endpoint de prueba
    @app.route('/api/test', methods=['GET'])
    def test():
        return jsonify({"message": "Hello from Render!"})

    with app.app_context():
        # Importa los blueprints
        from .routes.buildings import buildings_bp
        from .routes.systems import systems_bp
        from .routes.data import data_bp
        from .routes.commands import commands_bp
        from .routes.signals import signals_bp

        # Registra los blueprints
        app.register_blueprint(buildings_bp)
        app.register_blueprint(systems_bp)
        app.register_blueprint(data_bp)
        app.register_blueprint(commands_bp)
        app.register_blueprint(signals_bp)

        # Crea las tablas en la base de datos
        db.create_all()

        # Imprime las rutas registradas (para depuración)
        print("Registered blueprints:")
        for rule in app.url_map.iter_rules():
            print(f"{rule}")

    return app