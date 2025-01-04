from flask import Blueprint, jsonify, request
from app.models import DataCO2, DataPresurizacion
from app import db

data_bp = Blueprint('data', __name__, url_prefix='/api/data')

@data_bp.route('/co2/sistema/<int:sistema_id>', methods=['GET'])
def get_data_co2(sistema_id):
    data = DataCO2.query.filter_by(id_sistema=sistema_id).order_by(DataCO2.timestamp.desc()).limit(100).all()
    return jsonify([{
        'id': d.id,
        'timestamp': d.timestamp,
        'concentracion_co2': d.concentracion_co2,
        'presion': d.presion,
        'temperatura': d.temperatura
    } for d in data])

@data_bp.route('/presurizacion/<int:sistema_id>', methods=['GET'])
def get_data_presurizacion(sistema_id):
    data = DataPresurizacion.query.filter_by(id_sistema=sistema_id).order_by(DataPresurizacion.timestamp.desc()).limit(100).all()
    return jsonify([{
        'id': d.id,
        'timestamp': d.timestamp,
        'tensionMotor': d.tensionMotor,
        'tensionDC': d.tensionDC,
        'corriente': d.corriente,
        'potencia': d.potencia
    } for d in data])