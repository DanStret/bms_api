from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app import db

modes_bp = Blueprint('modes', __name__, url_prefix='/api/modes')

@modes_bp.route('/<int:id_sistema>', methods=['GET'])
def get_modes(id_sistema):
    try:
        query = text("""
            SELECT id_sistema, modo, fecha
            FROM modo 
            WHERE id_sistema = :id_sistema
            ORDER BY fecha DESC 
            LIMIT 1
        """)
        
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()

        if not result:
            return jsonify({
                "status": "error",
                "message": f"No se encontró modo para el sistema {id_sistema}"
            }), 404

        return jsonify({
            "status": "success",
            "data": {
                "id_sistema": result.id_sistema,
                "modo": result.modo,
                "fecha": result.fecha
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500