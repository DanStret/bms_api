from flask import Blueprint, jsonify, request
from app.models import Sistema, Equipo
from sqlalchemy import text
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
    
    
@systems_bp.route('/', methods=['GET'])
def get_sistemas_by_edificio_piso():
    try:
        id_edificio = request.args.get("id_edificio")
        id_piso = request.args.get("id_piso")

        if not id_edificio:
            return jsonify({"status": "error", "message": "Se requiere al menos el parámetro id_edificio"}), 400

        query = """
            SELECT s.id_sistema, s.nombre AS nombre_sistema, s.tipo, s.estatus, s.fecha_instalacion
            FROM sistemas s
            LEFT JOIN pisos p ON s.id_piso = p.id_piso
            LEFT JOIN edificios e ON p.id_edificio = e.id_edificio OR s.id_piso IS NULL
        """
        filters = ["e.id_edificio = :id_edificio"]
        params = {"id_edificio": id_edificio}

        if id_piso:
            filters.append("p.id_piso = :id_piso")
            params["id_piso"] = id_piso

        query += " WHERE " + " AND ".join(filters)
        result = db.session.execute(text(query), params).fetchall()

        sistemas = [
            {
                "id_sistema": row.id_sistema,
                "nombre_sistema": row.nombre_sistema,
                "tipo": row.tipo,
                "estatus": row.estatus,
                "fecha_instalacion": row.fecha_instalacion
            }
            for row in result
        ]
        return jsonify({"status": "success", "sistemas": sistemas}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@systems_bp.route('/detalle/<int:id_sistema>', methods=['GET'])
def get_sistema_detalle(id_sistema):
    try:
        query = text("""
            SELECT id_sistema, nombre, tipo, estatus, fecha_instalacion
            FROM sistemas
            WHERE id_sistema = :id_sistema
        """)
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()

        if not result:
            return jsonify({"status": "error", "message": "Sistema no encontrado"}), 404

        sistema = {
            "id_sistema": result.id_sistema,
            "nombre": result.nombre,
            "tipo": result.tipo,
            "estatus": result.estatus,
            "fecha_instalacion": result.fecha_instalacion,
        }
        return jsonify({"status": "success", "sistema": sistema}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500