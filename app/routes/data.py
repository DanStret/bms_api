from flask import Blueprint, jsonify, request
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

@data_bp.route('/co2/data/<int:id_sistema>', methods=['POST'])
def insert_data_co2(id_sistema):
    try:
        # Obtenemos los datos del cuerpo de la solicitud
        data = request.get_json()

        # Validación de los datos requeridos
        required_fields = ["tensionMotor", "tensionDC", "corriente", "potencia", 
                           "frecuencia", "temperatura", "AI", "contaminacion"]
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Falta el campo {field}"}), 400
        
        # Construcción de la consulta SQL para insertar los datos
        query = text("""
            INSERT INTO data_co2
            (id_sistema, timestamp, tensionMotor, tensionDC, corriente, potencia, 
            frecuencia, temperatura, AI, contaminacion)
            VALUES
            (:id_sistema, NOW(), :tensionMotor, :tensionDC, :corriente, :potencia,
            :frecuencia, :temperatura, :AI, :contaminacion)
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
            "AI": data["AI"],
            "contaminacion": data["contaminacion"]
        })
        db.session.commit()

        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@data_bp.route('/presurizacion/<int:id_sistema>', methods=['GET'])
def get_latest_data_presurizacion(id_sistema):
    try:
        query = text("""
            SELECT id, timestamp, tensionMotor, tensionDC, Corriente, Potencia, 
                   Frecuencia, Temperatura, IA, presion
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
            "presion": result.presion,
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
        

@data_bp.route('/chiller/principal/<int:id_sistema>', methods=['GET'])
def get_chiller_principal_data(id_sistema):
    try:
        query = text("""
            SELECT * FROM data_chiller_principal 
            WHERE id_sistema = :id_sistema
            ORDER BY timestamp DESC LIMIT 1
        """)
        result = db.session.execute(query, {"id_sistema": id_sistema}).fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "No hay datos"}), 404

        data = {
            "id": result.id,
            "id_chiller": result.id_chiller,
            "timestamp": result.timestamp,
            "temp_salida_agua": result.temp_salida_agua,
            "temp_entrada_agua": result.temp_entrada_agua,
            "temp_aire_ambiente": result.temp_aire_ambiente,
            "presion_succion_sys1": result.presion_succion_sys1,
            "presion_succion_sys2": result.presion_succion_sys2,
            "presion_descarga_sys1": result.presion_descarga_sys1,
            "presion_descarga_sys2": result.presion_descarga_sys2,
            "setpoint_salida_agua": result.setpoint_salida_agua,
            "setpoint_remoto": result.setpoint_remoto,
            "estado_sys1": result.estado_sys1,
            "estado_sys2": result.estado_sys2,
            "alarma_chiller": result.alarma_chiller,
            "encendido": result.encendido,
            "modo_control": result.modo_control
        }
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/principal/<int:id_sistema>', methods=['POST'])
def insert_chiller_principal_data(id_sistema):
    try:
        data = request.get_json()
        data['id_sistema'] = id_sistema
        
        query = text("""
            INSERT INTO data_chiller_principal (
                id_sistema, temp_salida_agua, temp_entrada_agua, temp_aire_ambiente,
                presion_succion_sys1, presion_succion_sys2, presion_descarga_sys1,
                presion_descarga_sys2, setpoint_salida_agua, setpoint_remoto,
                estado_sys1, estado_sys2, alarma_chiller, encendido, modo_control
            ) VALUES (
                :id_sistema, :temp_salida_agua, :temp_entrada_agua, :temp_aire_ambiente,
                :presion_succion_sys1, :presion_succion_sys2, :presion_descarga_sys1,
                :presion_descarga_sys2, :setpoint_salida_agua, :setpoint_remoto,
                :estado_sys1, :estado_sys2, :alarma_chiller, :encendido, :modo_control
            )
        """)
        
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/secundario/<int:id_chiller>', methods=['GET'])
def get_chiller_secundario_data(id_chiller):
    try:
        query = text("""
            SELECT * FROM data_chiller_secundario 
            WHERE id_chiller = :id_chiller
            ORDER BY timestamp DESC LIMIT 1
        """)
        result = db.session.execute(query, {"id_chiller": id_chiller}).fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "No hay datos"}), 404

        data = {
            "id": result.id,
            "id_chiller": result.id_chiller,
            "timestamp": result.timestamp,
            "temp_eductor_sys1": result.temp_eductor_sys1,
            "temp_eductor_sys2": result.temp_eductor_sys2,
            "horas_operacion_sys1": result.horas_operacion_sys1,
            "horas_operacion_sys2": result.horas_operacion_sys2,
            "codigo_operacion_sys1": result.codigo_operacion_sys1,
            "codigo_operacion_sys2": result.codigo_operacion_sys2,
            "codigo_falla_sys1": result.codigo_falla_sys1,
            "codigo_falla_sys2": result.codigo_falla_sys2,
            "sistema_lider": result.sistema_lider,
            "corte_salida_agua": result.corte_salida_agua,
            "apertura_valvula_economizer_sys1": result.apertura_valvula_economizer_sys1,
            "apertura_valvula_economizer_sys2": result.apertura_valvula_economizer_sys2,
            "corte_presion_succion": result.corte_presion_succion,
            "subcooling_sys1": result.subcooling_sys1,
            "subcooling_sys2": result.subcooling_sys2,
            "rango_enfriamiento_sc": result.rango_enfriamiento_sc,
            "superheat_descarga_sys1": result.superheat_descarga_sys1,
            "superheat_descarga_sys2": result.superheat_descarga_sys2,
            "presion_aceite_sys1": result.presion_aceite_sys1,
            "presion_aceite_sys2": result.presion_aceite_sys2,
            "estado_valvula_solenoide1_sys1": result.estado_valvula_solenoide1_sys1,
            "estado_valvula_solenoide1_sys2": result.estado_valvula_solenoide1_sys2,
            "estado_valvula_solenoide2_sys1": result.estado_valvula_solenoide2_sys1,
            "estado_valvula_solenoide2_sys2": result.estado_valvula_solenoide2_sys2,
            "tipo_liquido_enfriado": result.tipo_liquido_enfriado,
            "unidad_pantalla": result.unidad_pantalla,
            "bloqueo_sys1": result.bloqueo_sys1,
            "bloqueo_sys2": result.bloqueo_sys2,
            "apagado_suave": result.apagado_suave,
            "arranque_rapido": result.arranque_rapido,
            "opcion_limite_sonido": result.opcion_limite_sonido,
            "arranque_bomba_glycol": result.arranque_bomba_glycol
        }
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/secundario/<int:id_chiller>', methods=['POST'])
def insert_chiller_secundario_data(id_chiller):
    try:
        data = request.get_json()
        data['id_chiller'] = id_chiller
        
        query = text("""
            INSERT INTO data_chiller_secundario (
                id_chiller, temp_eductor_sys1, temp_eductor_sys2, horas_operacion_sys1,
                horas_operacion_sys2, codigo_operacion_sys1, codigo_operacion_sys2,
                codigo_falla_sys1, codigo_falla_sys2, sistema_lider, corte_salida_agua,
                apertura_valvula_economizer_sys1, apertura_valvula_economizer_sys2,
                corte_presion_succion, subcooling_sys1, subcooling_sys2,
                rango_enfriamiento_sc, superheat_descarga_sys1, superheat_descarga_sys2,
                presion_aceite_sys1, presion_aceite_sys2, estado_valvula_solenoide1_sys1,
                estado_valvula_solenoide1_sys2, estado_valvula_solenoide2_sys1,
                estado_valvula_solenoide2_sys2, tipo_liquido_enfriado, unidad_pantalla,
                bloqueo_sys1, bloqueo_sys2, apagado_suave, arranque_rapido,
                opcion_limite_sonido, arranque_bomba_glycol
            ) VALUES (
                :id_chiller, :temp_eductor_sys1, :temp_eductor_sys2, :horas_operacion_sys1,
                :horas_operacion_sys2, :codigo_operacion_sys1, :codigo_operacion_sys2,
                :codigo_falla_sys1, :codigo_falla_sys2, :sistema_lider, :corte_salida_agua,
                :apertura_valvula_economizer_sys1, :apertura_valvula_economizer_sys2,
                :corte_presion_succion, :subcooling_sys1, :subcooling_sys2,
                :rango_enfriamiento_sc, :superheat_descarga_sys1, :superheat_descarga_sys2,
                :presion_aceite_sys1, :presion_aceite_sys2, :estado_valvula_solenoide1_sys1,
                :estado_valvula_solenoide1_sys2, :estado_valvula_solenoide2_sys1,
                :estado_valvula_solenoide2_sys2, :tipo_liquido_enfriado, :unidad_pantalla,
                :bloqueo_sys1, :bloqueo_sys2, :apagado_suave, :arranque_rapido,
                :opcion_limite_sonido, :arranque_bomba_glycol
            )
        """)
        
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/condensador/<int:id_chiller>', methods=['GET'])
def get_condensador_data(id_chiller):
    try:
        query = text("""
            SELECT * FROM condensador 
            WHERE id_chiller = :id_chiller
            ORDER BY timestamp DESC LIMIT 1
        """)
        result = db.session.execute(query, {"id_chiller": id_chiller}).fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "No hay datos"}), 404

        data = {
            "id": result.id,
            "id_chiller": result.id_chiller,
            "timestamp": result.timestamp,
            "temp_condensador_sys1": result.temp_condensador_sys1,
            "temp_condensador_sys2": result.temp_condensador_sys2,
            "apertura_valvula_drenaje_sys1": result.apertura_valvula_drenaje_sys1,
            "apertura_valvula_drenaje_sys2": result.apertura_valvula_drenaje_sys2,
            "subcooling_sys1": result.subcooling_sys1,
            "subcooling_sys2": result.subcooling_sys2,
            "estado_ventiladores_sys1": result.estado_ventiladores_sys1,
            "estado_ventiladores_sys2": result.estado_ventiladores_sys2,
            "tipo_control_ventilador": result.tipo_control_ventilador
        }
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/condensador/<int:id_chiller>', methods=['POST'])
def insert_condensador_data(id_chiller):
    try:
        data = request.get_json()
        data['id_chiller'] = id_chiller
        
        query = text("""
            INSERT INTO condensador (
                id_chiller, temp_condensador_sys1, temp_condensador_sys2,
                apertura_valvula_drenaje_sys1, apertura_valvula_drenaje_sys2,
                subcooling_sys1, subcooling_sys2, estado_ventiladores_sys1,
                estado_ventiladores_sys2, tipo_control_ventilador
            ) VALUES (
                :id_chiller, :temp_condensador_sys1, :temp_condensador_sys2,
                :apertura_valvula_drenaje_sys1, :apertura_valvula_drenaje_sys2,
                :subcooling_sys1, :subcooling_sys2, :estado_ventiladores_sys1,
                :estado_ventiladores_sys2, :tipo_control_ventilador
            )
        """)
        
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/evaporador/<int:id_chiller>', methods=['GET'])
def get_evaporador_data(id_chiller):
    try:
        query = text("""
            SELECT * FROM evaporador 
            WHERE id_chiller = :id_chiller
            ORDER BY timestamp DESC LIMIT 1
        """)
        result = db.session.execute(query, {"id_chiller": id_chiller}).fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "No hay datos"}), 404

        data = {
            "id": result.id,
            "id_chiller": result.id_chiller,
            "timestamp": result.timestamp,
            "nivel_liquido_evaporador_sys1": result.nivel_liquido_evaporador_sys1,
            "nivel_liquido_evaporador_sys2": result.nivel_liquido_evaporador_sys2,
            "temp_salida_agua": result.temp_salida_agua,
            "temp_entrada_agua": result.temp_entrada_agua,
            "estado_ventilador": result.estado_ventilador,
            "estado_bomba": result.estado_bomba,
            "modo_operacion": result.modo_operacion
        }
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/evaporador/<int:id_chiller>', methods=['POST'])
def insert_evaporador_data(id_chiller):
    try:
        data = request.get_json()
        data['id_chiller'] = id_chiller
        
        query = text("""
            INSERT INTO evaporador (
                id_chiller, nivel_liquido_evaporador_sys1, nivel_liquido_evaporador_sys2,
                temp_salida_agua, temp_entrada_agua, estado_ventilador,
                estado_bomba, modo_operacion
            ) VALUES (
                :id_chiller, :nivel_liquido_evaporador_sys1, :nivel_liquido_evaporador_sys2,
                :temp_salida_agua, :temp_entrada_agua, :estado_ventilador,
                :estado_bomba, :modo_operacion
            )
        """)
        
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/compresor/<int:id_chiller>', methods=['GET'])
def get_compresor_data(id_chiller):
    try:
        query = text("""
            SELECT * FROM compresor 
            WHERE id_chiller = :id_chiller
            ORDER BY timestamp DESC LIMIT 1
        """)
        result = db.session.execute(query, {"id_chiller": id_chiller}).fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "No hay datos"}), 404

        data = {
            "id": result.id,
            "id_chiller": result.id_chiller,
            "timestamp": result.timestamp,
            "temp_vsd_ambiente": result.temp_vsd_ambiente,
            "temp_descarga_sys1": result.temp_descarga_sys1,
            "temp_descarga_sys2": result.temp_descarga_sys2,
            "corriente_fla_sys1": result.corriente_fla_sys1,
            "corriente_fla_sys2": result.corriente_fla_sys2,
            "arranques_compresor_sys1": result.arranques_compresor_sys1,
            "arranques_compresor_sys2": result.arranques_compresor_sys2,
            "temp_max_motor_sys1": result.temp_max_motor_sys1,
            "temp_max_motor_sys2": result.temp_max_motor_sys2,
            "frecuencia_salida_vsd": result.frecuencia_salida_vsd,
            "comando_frecuencia_vsd": result.comando_frecuencia_vsd,
            "voltaje_bus_dc": result.voltaje_bus_dc,
            "ajuste_sobrecorriente_sys1": result.ajuste_sobrecorriente_sys1,
            "ajuste_sobrecorriente_sys2": result.ajuste_sobrecorriente_sys2,
            "presion_succion_sys1": result.presion_succion_sys1,
            "presion_succion_sys2": result.presion_succion_sys2,
            "presion_descarga_sys1": result.presion_descarga_sys1,
            "presion_descarga_sys2": result.presion_descarga_sys2,
            "superheat_descarga_sys1": result.superheat_descarga_sys1,
            "superheat_descarga_sys2": result.superheat_descarga_sys2,
            "estado_arranque_sys1": result.estado_arranque_sys1,
            "estado_arranque_sys2": result.estado_arranque_sys2
        }
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/chiller/compresor/<int:id_chiller>', methods=['POST'])
def insert_compresor_data(id_chiller):
    try:
        data = request.get_json()
        data['id_chiller'] = id_chiller
        
        query = text("""
            INSERT INTO compresor (
                id_chiller, temp_vsd_ambiente, temp_descarga_sys1, temp_descarga_sys2,
                corriente_fla_sys1, corriente_fla_sys2, arranques_compresor_sys1,
                arranques_compresor_sys2, temp_max_motor_sys1, temp_max_motor_sys2,
                frecuencia_salida_vsd, comando_frecuencia_vsd, voltaje_bus_dc,
                ajuste_sobrecorriente_sys1, ajuste_sobrecorriente_sys2,
                presion_succion_sys1, presion_succion_sys2, presion_descarga_sys1,
                presion_descarga_sys2, superheat_descarga_sys1, superheat_descarga_sys2,
                estado_arranque_sys1, estado_arranque_sys2
            ) VALUES (
                :id_chiller, :temp_vsd_ambiente, :temp_descarga_sys1, :temp_descarga_sys2,
                :corriente_fla_sys1, :corriente_fla_sys2, :arranques_compresor_sys1,
                :arranques_compresor_sys2, :temp_max_motor_sys1, :temp_max_motor_sys2,
                :frecuencia_salida_vsd, :comando_frecuencia_vsd, :voltaje_bus_dc,
                :ajuste_sobrecorriente_sys1, :ajuste_sobrecorriente_sys2,
                :presion_succion_sys1, :presion_succion_sys2, :presion_descarga_sys1,
                :presion_descarga_sys2, :superheat_descarga_sys1, :superheat_descarga_sys2,
                :estado_arranque_sys1, :estado_arranque_sys2
            )
        """)
        
        db.session.execute(query, data)
        db.session.commit()
        return jsonify({"status": "success", "message": "Datos del compresor insertados correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500