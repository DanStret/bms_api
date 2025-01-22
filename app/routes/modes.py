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
        
@modes_bp.route('/mode/<int:id_sistema>', methods=['POST'])
def insert_mode(id_sistema):
    try:
        data = request.get_json()
        modo = data.get("modo")

        if modo not in ["Automatico", "Manual"]:
            return jsonify({"status": "error", "message": "Modo inválido ('Automatico' o 'Manual')"}), 400

        query = text("INSERT INTO modo (id_sistema, modo) VALUES (:id_sistema, :modo)")
        db.session.execute(query, {"id_sistema": id_sistema, "modo": modo})
        db.session.commit()

        return jsonify({"status": "success", "message": "Modo insertado", "data": {"id_sistema": id_sistema, "modo": modo}}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
