from flask import Blueprint, jsonify, request
from app.models import Sistema, Equipo, Piso, Edificio
from sqlalchemy import text
from app import db
import pymysql


systems_bp = Blueprint('systems', __name__, url_prefix='/api/systems')

# Obtener sistemas con filtros opcionales
@systems_bp.route('/', methods=['GET'])
def get_sistemas():
    try:
        id_edificio = request.args.get("id_edificio")
        id_piso = request.args.get("id_piso")

        if not id_edificio:
            return jsonify({"status": "error", "message": "Se requiere al menos el parámetro id_edificio"}), 400

        # Consulta dinámica
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

        # Agregar filtros dinámicos
        query += " WHERE " + " AND ".join(filters)

        result = db.session.execute(text(query), params).fetchall()

        sistemas = [
            {"id_sistema": row.id_sistema, "nombre_sistema": row.nombre_sistema, "tipo": row.tipo,
             "estatus": row.estatus, "fecha_instalacion": row.fecha_instalacion}
            for row in result
        ]
        return jsonify({"status": "success", "sistemas": sistemas}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener sistemas: {str(e)}"}), 500

# Obtener sistemas por piso específico
@systems_bp.route('/piso/<int:id_piso>', methods=['GET'])
def get_sistemas_por_piso(id_piso):
    try:
        sistemas = Sistema.query.filter_by(id_piso=id_piso).all()
        return jsonify({
            "status": "success",
            "sistemas": [{
                'id_sistema': s.id_sistema,
                'nombre': s.nombre,
                'tipo': s.tipo,
                'estatus': s.estatus,
                'id_piso': s.id_piso
            } for s in sistemas]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener sistemas del piso: {str(e)}"
        }), 500

# Obtener equipos de un sistema
@systems_bp.route('/equipo/sistema/<int:id_sistema>', methods=['GET'])
def get_equipos_sistema(id_sistema):
    try:
        equipos = Equipo.query.filter_by(id_sistema=id_sistema).all()
        return jsonify({
            "status": "success",
            "equipos": [{
                'id_equipo': e.id_equipo,
                'nombre': e.nombre,
                'marca': e.marca,
                'modelo': e.modelo,
                'estatus': e.estatus
            } for e in equipos]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener equipos: {str(e)}"
        }), 500

# Obtener sistemas por edificio y piso
@systems_bp.route('/edificio/<int:id_edificio>/piso/<int:id_piso>', methods=['GET'])
def get_sistemas_por_edificio_y_piso(id_edificio, id_piso):
    try:
        sistemas = Sistema.query.join(Piso).filter(
            Piso.id_edificio == id_edificio,
            Sistema.id_piso == id_piso
        ).all()
        
        return jsonify({
            "status": "success",
            "sistemas": [{
                'id_sistema': s.id_sistema,
                'nombre': s.nombre,
                'tipo': s.tipo,
                'estatus': s.estatus
            } for s in sistemas]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Obtener detalle de un sistema específico
@systems_bp.route('/detalle/<int:id_sistema>', methods=['GET'])
def get_sistema_detalle(id_sistema):
    try:
        sistema = Sistema.query.get(id_sistema)
        if not sistema:
            return jsonify({
                "status": "error",
                "message": "Sistema no encontrado"
            }), 404

        return jsonify({
            "status": "success",
            "sistema": {
                "id_sistema": sistema.id_sistema,
                "nombre": sistema.nombre,
                "tipo": sistema.tipo,
                "estatus": sistema.estatus,
                "fecha_instalacion": sistema.fecha_instalacion,
                "id_piso": sistema.id_piso
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
        
    