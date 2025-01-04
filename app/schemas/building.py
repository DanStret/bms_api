from app import ma
from app.models.building import Edificio, Piso

class PisoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Piso

    id_piso = ma.auto_field()
    nombre = ma.auto_field()
    ubicacion = ma.auto_field()
    id_edificio = ma.auto_field()

class EdificioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Edificio

    id_edificio = ma.auto_field()
    nombre = ma.auto_field()
    direccion = ma.auto_field()
    ubicacion = ma.auto_field()
    estatus = ma.auto_field()
    fecha_creacion = ma.auto_field()
    pisos = ma.Nested(PisoSchema, many=True)

edificio_schema = EdificioSchema()
edificios_schema = EdificioSchema(many=True)
piso_schema = PisoSchema()
pisos_schema = PisoSchema(many=True)