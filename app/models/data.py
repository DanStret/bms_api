from app import db
from datetime import datetime

class DataCO2(db.Model):
    __tablename__ = 'data_co2'
    id = db.Column(db.Integer, primary_key=True)
    id_sistema = db.Column(db.Integer, db.ForeignKey('sistemas.id_sistema'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    concentracion_co2 = db.Column(db.Float)
    presion = db.Column(db.Float)
    temperatura = db.Column(db.Float)
    flujo_aire = db.Column(db.Float)

class DataPresurizacion(db.Model):
    __tablename__ = 'data_presurizacion'
    id = db.Column(db.Integer, primary_key=True)
    id_sistema = db.Column(db.Integer, db.ForeignKey('sistemas.id_sistema'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    tensionMotor = db.Column(db.Float)
    tensionDC = db.Column(db.Float)
    corriente = db.Column(db.Float)
    potencia = db.Column(db.Float)
    frecuencia = db.Column(db.Float)
    temperatura = db.Column(db.Float)
    IA = db.Column(db.Float)
    AV = db.Column(db.Float)