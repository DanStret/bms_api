from app import db
from datetime import datetime

class Edificio(db.Model):
    __tablename__ = 'edificios'
    id_edificio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    ubicacion = db.Column(db.String(255))
    estatus = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    pisos = db.relationship('Piso', backref='edificio', lazy=True)

class Piso(db.Model):
    __tablename__ = 'pisos'
    id_piso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    id_edificio = db.Column(db.Integer, db.ForeignKey('edificios.id_edificio'), nullable=False)
    ubicacion = db.Column(db.String(255))