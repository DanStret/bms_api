from flask import Flask, jsonify ,render_template
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
        from.routes.modes import modes_bp

        # Registra los blueprints
        app.register_blueprint(buildings_bp)
        app.register_blueprint(systems_bp)
        app.register_blueprint(data_bp)
        app.register_blueprint(commands_bp)
        app.register_blueprint(signals_bp)
        app.register_blueprint(modes_bp)

    def get_endpoint_docs(endpoint, view_func, rule):
        """Obtiene la documentación completa de un endpoint."""
        docs = {
            'endpoint': endpoint,
            'methods': sorted(list(rule.methods - {'OPTIONS', 'HEAD'})),
            'path': rule.rule,
            'description': view_func.__doc__,
            'auth_required': hasattr(view_func, 'token_required'),
            'params': []
        }

        # Detectar parámetros de URL
        for arg in rule.arguments:
            docs['params'].append({
                'name': arg,
                'type': 'path',
                'required': True
            })

        return docs

    @app.route('/')
    def api_docs():
        groups = {
            'Autenticación': [],
            'Edificios': [],
            'Sistemas': [],
            'Datos': [],
            'Comandos': [],
            'Señales': [],
            'Modos': []
        }

        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':
                continue

            view_func = app.view_functions[rule.endpoint]
            blueprint = rule.endpoint.split('.')[0]

            endpoint_info = {
                'methods': sorted(list(rule.methods - {'OPTIONS', 'HEAD'})),
                'path': rule.rule,
                'description': view_func.__doc__,
                'auth_required': hasattr(view_func, 'token_required')
            }

            if blueprint == 'auth':
                groups['Autenticación'].append(endpoint_info)
            elif blueprint == 'buildings':
                groups['Edificios'].append(endpoint_info)
            elif blueprint == 'systems':
                groups['Sistemas'].append(endpoint_info)
            elif blueprint == 'data':
                groups['Datos'].append(endpoint_info)
            elif blueprint == 'commands':
                groups['Comandos'].append(endpoint_info)
            elif blueprint == 'signals':
                groups['Señales'].append(endpoint_info)
            elif blueprint == 'modes':
                groups['Modos'].append(endpoint_info)

        return render_template('index.html', groups=groups)

    return app