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
    

@data_bp.route('/presurizacion/data/<int:id_sistema>', methods=['POST'])
def insert_data_presurizacion(id_sistema):
    try:
        # Obtenemos los datos del cuerpo de la solicitud
        data = request.get_json()

        # Validación de los datos requeridos
        required_fields = ["tensionMotor", "tensionDC", "corriente", "potencia", 
                           "frecuencia", "temperatura", "IA", "AV"]
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Falta el campo {field}"}), 400
        
        # Construcción de la consulta SQL para insertar los datos
        query = text("""
            INSERT INTO data_presurizacion
            (id_sistema, timestamp, tensionMotor, tensionDC, corriente, potencia, 
            frecuencia, temperatura, IA, AV)
            VALUES
            (:id_sistema, NOW(), :tensionMotor, :tensionDC, :corriente, :potencia,
            :frecuencia, :temperatura, :IA, :AV)
        """)

        # Ejecutamos la consulta con los datos recibidos
        db.session.execute(query, {
            "id_sistema": id_sistema,  # Usamos el id_sistema de la URL
            "tensionMotor": data["tensionMotor"],
            "tensionDC": data["tensionDC"],
            "corriente": data["corriente"],
            "potencia": data["potencia"],
            "frecuencia": data["frecuencia"],
            "temperatura": data["temperatura"],
            "IA": data["IA"],
            "AV": data["AV"]
        })
        db.session.commit()

        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@data_bp.route('/fancoil/<int:id_sistema>', methods=['GET'])
def get_latest_data_fancoil(id_sistema):
    try:
        query = text("""
            SELECT id_sistema, timestamp, temp_amb , temp_setpoint , estado_valvula ,
            fan_speed , modo_trabajo , on_off , bloqueo 
            from data_fancoil 
            where id_sistema = :id_sistema 
            ORDER BY timestamp DESC LIMIT 1

        """)
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()

        if not result:
            return jsonify({
                "status": "error", 
                "message": "No se encontraron datos para el sistema especificado"
            }), 404

        data = {
            "id_sistema": result.id_sistema,
            "temp_amb": result.temp_amb,
            "temp_setpoint": result.temp_setpoint,
            "estado_valvula": result.estado_valvula,
            "fan_speed": result.fan_speed,
            "modo_trabajo": result.modo_trabajo,
            "on_off": result.on_off,
            "bloqueo": result.bloqueo,
        }
        return jsonify({"status": "success", "data_fancoil": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@data_bp.route('/fancoil/data/<int:id_sistema>', methods=['POST'])
def insert_data_fancoil(id_sistema):
    try:
        # Obtenemos los datos del cuerpo de la solicitud
        data = request.get_json()

        # Validación de los datos requeridos
        required_fields = ["temp_amb", "temp_setpoint", "estado_valvula", 
                         "fan_speed", "modo_trabajo", "on_off", "bloqueo"]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error", 
                    "message": f"Falta el campo {field}"
                }), 400
        
        # Construcción de la consulta SQL para insertar los datos
        query = text("""
            INSERT INTO data_fancoil
            (id_sistema, timestamp, temp_amb, temp_setpoint, estado_valvula,
            fan_speed, modo_trabajo, on_off, bloqueo)
            VALUES
            (:id_sistema, NOW(), :temp_amb, :temp_setpoint, :estado_valvula,
            :fan_speed, :modo_trabajo, :on_off, :bloqueo)
        """)

        # Ejecutamos la consulta con los datos recibidos
        db.session.execute(query, {
            "id_sistema": id_sistema,
            "temp_amb": data["temp_amb"],
            "temp_setpoint": data["temp_setpoint"],
            "estado_valvula": data["estado_valvula"],
            "fan_speed": data["fan_speed"],
            "modo_trabajo": data["modo_trabajo"],
            "on_off": data["on_off"],
            "bloqueo": data["bloqueo"]
        })
        db.session.commit()

        return jsonify({
            "status": "success", 
            "message": "Datos del fancoil insertados correctamente"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error", 
            "message": f"Error al insertar datos: {str(e)}"
        }), 500