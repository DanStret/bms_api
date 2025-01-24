from flask import Blueprint, jsonify, request
from app.models import Edificio, Piso
from sqlalchemy import text
from app import db
from flask_cors import cross_origin

buildings_bp = Blueprint('buildings', __name__, url_prefix='/api/buildings')

@buildings_bp.after_request
def after_buildings_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Decorador para todas las rutas
@buildings_bp.route('/', methods=['OPTIONS'])
@cross_origin()
def handle_preflight():
    response = jsonify({'status': 'ok'})
    return response

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

@buildings_bp.route('/pisos', methods=['GET'])
def get_pisos_by_edificio():
    try:
        id_edificio = request.args.get("id_edificio")
        if not id_edificio:
            return jsonify({"status": "error", "message": "Se requiere el parámetro id_edificio"}), 400

        query = text("""
            SELECT id_piso, nombre
            FROM pisos
            WHERE id_edificio = :id_edificio
        """)
        result = db.session.execute(query, {"id_edificio": id_edificio}).fetchall()

        pisos = [{"id_piso": row.id_piso, "nombre": row.nombre} for row in result]
        return jsonify({"status": "success", "pisos": pisos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener pisos: {str(e)}"}), 500
    
    
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
    
    

