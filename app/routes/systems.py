from flask import Blueprint, jsonify
from app.models import Sistema, Equipo
from app import db

systems_bp = Blueprint('systems', __name__, url_prefix='/api/systems')

@systems_bp.route('/', methods=['GET'])
def get_sistemas():
    sistemas = Sistema.query.all()
    return jsonify([{
        'id_sistema': s.id_sistema,
        'nombre': s.nombre,
        'tipo': s.tipo,
        'estatus': s.estatus
    } for s in sistemas])

@systems_bp.route('/piso/<int:id_piso>', methods=['GET'])
def get_sistemas_por_piso(id_piso):
    sistemas = Sistema.query.filter_by(id_piso=id_piso).all()
    return jsonify([{
        'id_sistema': s.id_sistema,
        'nombre': s.nombre,
        'tipo': s.tipo,
        'estatus': s.estatus
    } for s in sistemas])

@systems_bp.route('/equipo/sistema/<int:id_sistema>', methods=['GET'])
def get_equipos_sistema(id_sistema):
    equipos = Equipo.query.filter_by(id_sistema=id_sistema).all()
    return jsonify([{
        'id_equipo': e.id_equipo,
        'nombre': e.nombre,
        'marca': e.marca,
        'modelo': e.modelo,
        'estatus': e.estatus
    } for e in equipos])