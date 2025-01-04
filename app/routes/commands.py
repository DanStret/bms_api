from flask import Blueprint, jsonify, request
from app.models import Comando
from app import db

commands_bp = Blueprint('commands', __name__, url_prefix='/api/commands')

@commands_bp.route('/', methods=['POST'])
def create_comando():
    data = request.get_json()
    nuevo_comando = Comando(
        id_sistema=data['id_sistema'],
        id_usuario=data['id_usuario'],
        tipo_comando=data['tipo_comando'],
        detalles=data.get('detalles', {})
    )
    db.session.add(nuevo_comando)
    db.session.commit()
    return jsonify({'message': 'Comando creado'}), 201

@commands_bp.route('/usuario/<int:id_usuario>', methods=['GET'])
def get_comandos_usuario(id_usuario):
    comandos = Comando.query.filter_by(id_usuario=id_usuario).order_by(Comando.fecha.desc()).all()
    return jsonify([{
        'id_comando': c.id_comando,
        'tipo_comando': c.tipo_comando,
        'detalles': c.detalles,
        'fecha': c.fecha
    } for c in comandos])