from flask import Blueprint, jsonify, request
from app.models import Sistema, Equipo, Piso, Edificio
from sqlalchemy import text
from app import db
from datetime import datetime
import locale
import json
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
        


@systems_bp.route('/types', methods=['GET'])
def get_tipos_sistemas():
    try:
        id_edificio = request.args.get("id_edificio")
        id_piso = request.args.get("id_piso")
        
        if not id_edificio or not id_piso:
            return jsonify({"error": "Se requieren id_edificio e id_piso"}), 400

        query = text("""
            SELECT DISTINCT tipo
            FROM sistemas s
            JOIN pisos p ON s.id_piso = p.id_piso 
            WHERE p.id_edificio = :id_edificio 
            AND p.id_piso = :id_piso
        """)

        result = db.session.execute(query, {
            "id_edificio": id_edificio,
            "id_piso": id_piso
        })
        tipos = [row.tipo for row in result]

        return jsonify({"status": "success", "tipos": tipos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@systems_bp.route('/by-type', methods=['GET'])
def get_sistemas_by_tipo():
   try:
       id_edificio = request.args.get("id_edificio")
       id_piso = request.args.get("id_piso")
       tipo = request.args.get("tipo")

       if not all([id_edificio, id_piso, tipo]):
           return jsonify({"error": "Se requieren id_edificio, id_piso y tipo"}), 400

       query = text("""
           SELECT s.id_sistema, s.nombre, s.estatus, s.fecha_instalacion
            FROM sistemas s
            JOIN pisos p ON s.id_piso = p.id_piso
            WHERE p.id_edificio = :id_edificio 
            AND p.id_piso = :id_piso 
            AND s.tipo = :tipo
            AND s.estatus = 'Activo';
       """)

       result = db.session.execute(query, {
           "id_edificio": id_edificio,
           "id_piso": id_piso,
           "tipo": tipo
       })

       sistemas = [{
           "id_sistema": row.id_sistema,
           "nombre": row.nombre,
           "estatus": row.estatus,
           "tipo": tipo,
           "fecha_instalacion": row.fecha_instalacion.strftime("%d de %B de %Y %H:%M:%S") if row.fecha_instalacion else None
       } for row in result]

       return jsonify({"status": "success", "sistemas": sistemas}), 200
   except Exception as e:
       return jsonify({"status": "error", "message": str(e)}), 500
   
   
@systems_bp.route('/fancoil', methods=['GET'])
def get_fancoil_by_piso_and_edificio():
    try:
        # Parámetros de filtro
        id_edificio = request.args.get("id_edificio", type=int)
        id_piso = request.args.get("id_piso", type=int)

        # Validación de id_edificio
        if not id_edificio:
            return jsonify({
                "status": "error",
                "message": "Se requiere el parámetro id_edificio."
            }), 400

        # Construcción dinámica del filtro SQL
        query_base = """
            SELECT 
                e.nombre AS edificio,
                p.nombre AS piso,
                s.nombre AS nombre,
                s.id_sistema,
                s.tipo,
                s.estatus,
                s.fecha_instalacion
            FROM 
                edificios e
            JOIN 
                pisos p ON e.id_edificio = p.id_edificio
            JOIN 
                sistemas s ON p.id_piso = s.id_piso
            WHERE 
                s.tipo = 'Fancoil'
                AND e.id_edificio = :id_edificio
        """

        if id_piso:
            query_base += " AND p.id_piso = :id_piso"

        # Crear consulta final
        query = text(query_base)

        # Ejecutar la consulta con los parámetros apropiados
        params = {"id_edificio": id_edificio}
        if id_piso:
            params["id_piso"] = id_piso

        result = db.session.execute(query, params).fetchall()

        # Construcción de la respuesta
        fancoil_systems = [{
            "edificio": row.edificio,
            "piso": row.piso,
            "id_sistema": row.id_sistema,
            "nombre": row.nombre,
            "tipo": row.tipo,
            "estatus": row.estatus,
            "fecha_instalacion": row.fecha_instalacion.isoformat() if row.fecha_instalacion else None
        } for row in result]

        return jsonify({
            "status": "success",
            "sistemas": fancoil_systems
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener sistemas Fancoil: {str(e)}"
        }), 500