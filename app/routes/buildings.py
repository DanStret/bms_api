from flask import Blueprint, jsonify, request
from app.models import Edificio, Piso
from app import db

buildings_bp = Blueprint('buildings', __name__, url_prefix='/api/buildings')


# Get all buildings
@buildings_bp.route('/', methods=['GET'])
def get_edificios():
    edificios = Edificio.query.all()
    return jsonify([{
        'id_edificio': e.id_edificio,
        'nombre': e.nombre,
        'direccion': e.direccion,
        'ubicacion': e.ubicacion,
        'estatus': e.estatus,
        'pisos': [{
            'id_piso': p.id_piso,
            'nombre': p.nombre,
            'ubicacion': p.ubicacion
        } for p in e.pisos]
    } for e in edificios])

@buildings_bp.route('/<int:id_edificio>', methods=['GET'])
def get_edificio(id_edificio):
    edificio = Edificio.query.get_or_404(id_edificio)
    return jsonify({
        'id_edificio': edificio.id_edificio,
        'nombre': edificio.nombre,
        'direccion': edificio.direccion,
        'ubicacion': edificio.ubicacion,
        'estatus': edificio.estatus
    })

# Create new building
@buildings_bp.route('/', methods=['POST'])
def crear_edificio():
    data = request.get_json()
    nuevo_edificio = Edificio(
        nombre=data['nombre'],
        direccion=data['direccion'],
        ubicacion=data.get('ubicacion'),  # opcional
        estatus='Activo'
    )
    try:
        db.session.add(nuevo_edificio)
        db.session.commit()
        return jsonify({
            'message': 'Edificio creado exitosamente',
            'edificio': {
                'id_edificio': nuevo_edificio.id_edificio,
                'nombre': nuevo_edificio.nombre,
                'direccion': nuevo_edificio.direccion,
                'ubicacion': nuevo_edificio.ubicacion,
                'estatus': nuevo_edificio.estatus
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400