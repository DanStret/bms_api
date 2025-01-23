from flask import Blueprint, jsonify,request
from app.models import Señal
from sqlalchemy import text
from app import db

signals_bp = Blueprint('signals', __name__, url_prefix='/api/signals')

@signals_bp.route('/activas', methods=['GET'])
def get_señales_activas():
    señales = Señal.query.filter_by(estatus='Activo').all()
    return jsonify([{
        'id_señal': s.id_señal,
        'id_sistema': s.id_sistema,
        'tipo_señal': s.tipo_señal,
        'fecha': s.fecha
    } for s in señales])

# Cambiamos 'tipo_señal' por 'tipo'
@signals_bp.route('/tipo/<tipo>', methods=['GET'])
def get_señales_por_tipo(tipo):
    señales = Señal.query.filter_by(tipo_señal=tipo).all()
    return jsonify([{
        'id_señal': s.id_señal,
        'id_sistema': s.id_sistema,
        'estatus': s.estatus,
        'fecha': s.fecha
    } for s in señales])

@signals_bp.route('/sistema/<int:sistema_id>', methods=['GET'])
def get_señales_sistema(sistema_id):
    señales = Señal.query.filter_by(id_sistema=sistema_id).order_by(Señal.fecha.desc()).all()
    return jsonify([{
        'id_señal': s.id_señal,
        'tipo_señal': s.tipo_señal,
        'estatus': s.estatus,
        'fecha': s.fecha
    } for s in señales])
    
@signals_bp.route('/<int:id_sistema>', methods=['GET'])
def get_signals(id_sistema):
    try:
        # Obtener últimas señales
        query_señales = """
        SELECT s1.*
        FROM señales s1
        INNER JOIN (
            SELECT tipo_señal, MAX(fecha) as max_fecha
            FROM señales
            WHERE id_sistema = :id_sistema
            GROUP BY tipo_señal
        ) s2 ON s1.tipo_señal = s2.tipo_señal AND s1.fecha = s2.max_fecha
        WHERE s1.id_sistema = :id_sistema
        """
        
        # Obtener último estado
        query_estado = """
        SELECT * FROM estados 
        WHERE id_sistema = :id_sistema
        ORDER BY fecha DESC 
        LIMIT 1
        """
        
        señales = db.session.execute(text(query_señales), {"id_sistema": id_sistema}).fetchall()
        estado = db.session.execute(text(query_estado), {"id_sistema": id_sistema}).fetchone()
        
        # Formatear datos de presurización
        data_signals = {
            "señales": [{
                "tipo_señal": señal.tipo_señal,
                "estatus": señal.estatus
            } for señal in señales],
            "estado": {
                "estado": estado.estado if estado else "Parada"
            }
        }
        
        return jsonify({
            "status": "success",
            "data_signals": data_signals
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener datos de presurización: {str(e)}"
        }), 500
        
@signals_bp.route('/insert/signal/<int:id_sistema>', methods=['POST'])
def insertar_señal(id_sistema):
    try:
        data = request.get_json()

        
        required_fields = ["tipo_señal", "estatus"]
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Falta el campo {field}"}), 400
            
        query = text("""
            INSERT INTO señales(id_sistema,tipo_señal,estatus)
            VALUES
            (:id_sistema,:tipo_señal,:estatus);
        """)

        db.session.execute(query, {
            "id_sistema": id_sistema,  # Usamos el id_sistema de la URL
            "tipo_señal": data["tipo_señal"],
            "estatus": data["estatus"],
        })
        db.session.commit()

        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
@signals_bp.route('/insert/estado/<int:id_sistema>', methods=['POST'])
def insertar_estado(id_sistema):
    try:
        data = request.get_json()

            
        required_fields = ["estado"]
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Falta el campo {field}"}), 400
                
        query = text("""
                INSERT INTO estados(id_sistema,estado)
                VALUES
             (:id_sistema,:estado);
        """)

        db.session.execute(query, {
                "id_sistema": id_sistema,  # Usamos el id_sistema de la URL
                "estado": data["estado"],
        })
        db.session.commit()

        return jsonify({"status": "success", "message": "Datos insertados correctamente"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500