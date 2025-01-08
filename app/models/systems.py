from app import db
from datetime import datetime
from sqlalchemy import Enum

TIPO_SISTEMA = ['Presurizacion', 'CO2', 'Bomba Presion', 'Fancoil', 'Chiller']


class Sistema(db.Model):
    __tablename__ = 'sistemas'
    print("Tipos de sistema permitidos:", ['Presurizacion', 'CO2', 'Bomba Presion', 'Fancoil', 'Chiller'])
    id_sistema = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(Enum('Presurizacion', 'CO2', 'Bomba Presion', 'Fancoil', 'Chiller', name='sistema_tipo_enum'), nullable=False)

    id_edificio = db.Column(db.Integer, db.ForeignKey('edificios.id_edificio'))
    id_piso = db.Column(db.Integer, db.ForeignKey('pisos.id_piso'))
    estatus = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    fecha_instalacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    equipos = db.relationship('Equipo', backref='sistema', lazy=True)
    datos_co2 = db.relationship('DataCO2', backref='sistema', lazy=True)
    datos_presurizacion = db.relationship('DataPresurizacion', backref='sistema', lazy=True)
    datos_fancoil = db.relationship('DataFanCoil', backref='sistema', lazy=True)


class Equipo(db.Model):
    __tablename__ = 'equipos'
    id_equipo = db.Column(db.Integer, primary_key=True)
    id_sistema = db.Column(db.Integer, db.ForeignKey('sistemas.id_sistema'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    estatus = db.Column(Enum('Activo', 'Inactivo'), default='Activo')
    fecha_instalacion = db.Column(db.DateTime, default=datetime.utcnow)