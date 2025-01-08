from flask import Blueprint, jsonify, request
from app.models import DataCO2, DataPresurizacion
from sqlalchemy import text
from app import db

data_bp = Blueprint('data', __name__, url_prefix='/api/data')

@data_bp.route('/co2/<int:id_sistema>', methods=['GET'])
def get_data_co2(id_sistema):
    try:
        query = text("""
            SELECT id, timestamp, tensionMotor, tensionDC, Corriente, Potencia, 
                   Frecuencia, Temperatura, AI ,contaminacion
            FROM data_co2
            WHERE id_sistema = :id_sistema
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()

        if not result:
            return jsonify({
                "status": "error", 
                "message": "No se encontraron datos para el sistema especificado"
            }), 404

        data = {
            "id": result.id,
            "timestamp": result.timestamp,
            "tensionMotor": result.tensionMotor,
            "tensionDC": result.tensionDC,
            "corriente": result.Corriente,
            "potencia": result.Potencia,
            "frecuencia": result.Frecuencia,
            "temperatura": result.Temperatura,
            "AI": result.AI,
            "contaminacion": result.contaminacion,
        }
        return jsonify({"status": "success", "data_co2": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/presurizacion/<int:id_sistema>', methods=['GET'])
def get_latest_data_presurizacion(id_sistema):
    try:
        query = text("""
            SELECT id, timestamp, tensionMotor, tensionDC, Corriente, Potencia, 
                   Frecuencia, Temperatura, IA, AV
            FROM data_presurizacion
            WHERE id_sistema = :id_sistema
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()

        if not result:
            return jsonify({
                "status": "error", 
                "message": "No se encontraron datos para el sistema especificado"
            }), 404

        data = {
            "id": result.id,
            "timestamp": result.timestamp,
            "tensionMotor": result.tensionMotor,
            "tensionDC": result.tensionDC,
            "corriente": result.Corriente,
            "potencia": result.Potencia,
            "frecuencia": result.Frecuencia,
            "temperatura": result.Temperatura,
            "IA": result.IA,
            "AV": result.AV,
        }
        return jsonify({"status": "success", "data_presurizacion": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500