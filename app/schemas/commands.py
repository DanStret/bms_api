from app import ma
from app.models import Comando, Sistema, Usuario

class SistemaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Sistema
    
    id_sistema = ma.auto_field()
    nombre = ma.auto_field()

class UsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
    
    id_usuario = ma.auto_field()
    correo = ma.auto_field()

class ComandoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comando

    id_comando = ma.auto_field()
    id_sistema = ma.auto_field()
    id_usuario = ma.auto_field()
    tipo_comando = ma.auto_field()
    detalles = ma.auto_field()
    fecha = ma.auto_field()
    
    sistema = ma.Nested(SistemaSchema)
    usuario = ma.Nested(UsuarioSchema)

comando_schema = ComandoSchema()
comandos_schema = ComandoSchema(many=True)