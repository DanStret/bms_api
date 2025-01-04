from app import db
from datetime import datetime

class Comando(db.Model):
    __tablename__ = 'comandos'
    id_comando = db.Column(db.Integer, primary_key=True)
    id_sistema = db.Column(db.Integer, db.ForeignKey('sistemas.id_sistema'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo_comando = db.Column(db.Enum('Prender', 'Apagar', 'Cambiar Modo', 'Otro'), nullable=False)
    detalles = db.Column(db.JSON)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    sistema = db.relationship('Sistema', backref='comandos', lazy=True)
    usuario = db.relationship('Usuario', backref='comandos', lazy=True)