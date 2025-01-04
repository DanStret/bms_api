from flask import Blueprint, jsonify
from app.models import Señal
from app import db

signals_bp = Blueprint('signals', __name__, url_prefix='/api/signals')

@signals_bp.route('/activas', methods=['GET'])
def get_señales_activas():
    señales = Señal.query.filter_by(estatus='Activo').all()
    return jsonify([{
        'id_señal': s.id_señal,
        'id_sistema': s.id_sistema,
        'tipo_señal': s.tipo_señal,
        'fecha': s.fecha
    } for s in señales])

# Cambiamos 'tipo_señal' por 'tipo'
@signals_bp.route('/tipo/<tipo>', methods=['GET'])
def get_señales_por_tipo(tipo):
    señales = Señal.query.filter_by(tipo_señal=tipo).all()
    return jsonify([{
        'id_señal': s.id_señal,
        'id_sistema': s.id_sistema,
        'estatus': s.estatus,
        'fecha': s.fecha
    } for s in señales])

@signals_bp.route('/sistema/<int:sistema_id>', methods=['GET'])
def get_señales_sistema(sistema_id):
    señales = Señal.query.filter_by(id_sistema=sistema_id).order_by(Señal.fecha.desc()).all()
    return jsonify([{
        'id_señal': s.id_señal,
        'tipo_señal': s.tipo_señal,
        'estatus': s.estatus,
        'fecha': s.fecha
    } for s in señales])