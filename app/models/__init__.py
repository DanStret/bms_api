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
    pisos = db.relationship('Piso', backref='edificio', lazy=True)

class Piso(db.Model):
    __tablename__ = 'pisos'
    id_piso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    id_edificio = db.Column(db.Integer, db.ForeignKey('edificios.id_edificio'), nullable=False)
    ubicacion = db.Column(db.String(255))

class Sistema(db.Model):
    __tablename__ = 'sistemas'
    id_sistema = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.Enum('Presurización', 'CO2', 'Bomba Presión', 'Otro'), nullable=False)
    id_piso = db.Column(db.Integer, db.ForeignKey('pisos.id_piso'), nullable=False)
    estatus = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    fecha_instalacion = db.Column(db.DateTime, default=datetime.utcnow)

class Equipo(db.Model):
    __tablename__ = 'equipos'
    id_equipo = db.Column(db.Integer, primary_key=True)
    id_sistema = db.Column(db.Integer, db.ForeignKey('sistemas.id_sistema'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.Enum('Operativo', 'En Mantenimiento', 'Falla', 'Inactivo'), default='Operativo')
    fecha_instalacion = db.Column(db.DateTime, default=datetime.utcnow)

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

class Señal(db.Model):
    __tablename__ = 'señales'
    id_señal = db.Column(db.Integer, primary_key=True)
    id_sistema = db.Column(db.Integer, db.ForeignKey('sistemas.id_sistema'), nullable=False)
    tipo_señal = db.Column(db.Enum('BMS', 'Humo', 'Incendio', 'Otro'), nullable=False)
    estatus = db.Column(db.Enum('Activo', 'Inactivo'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class DataUsuario(db.Model):
    __tablename__ = 'data_usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(50), nullable=False)
    segundo_nombre = db.Column(db.String(50))
    primer_apellido = db.Column(db.String(50), nullable=False)
    segundo_apellido = db.Column(db.String(50))
    dni = db.Column(db.String(20), unique=True, nullable=False)
    edad = db.Column(db.Integer)
    sexo = db.Column(db.Enum('Masculino', 'Femenino', 'Otro'))
    especialidad = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable=False, unique=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo de Comando que faltaba
class Comando(db.Model):
    __tablename__ = 'comandos'
    id_comando = db.Column(db.Integer, primary_key=True)
    id_sistema = db.Column(db.Integer, db.ForeignKey('sistemas.id_sistema'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo_comando = db.Column(db.Enum('Prender', 'Apagar', 'Cambiar Modo', 'Otro'), nullable=False)
    detalles = db.Column(db.JSON)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    sistema = db.relationship('Sistema', backref='comandos')
    usuario = db.relationship('Usuario', backref='comandos')

# Usuario necesario para la relación con Comando
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')