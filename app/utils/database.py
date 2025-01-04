from app import db
from app.models.building import Edificio, Piso

class EdificioService:
    @staticmethod
    def get_all_edificios():
        return Edificio.query.all()

    @staticmethod
    def get_edificio_by_id(edificio_id):
        return Edificio.query.get_or_404(edificio_id)

    @staticmethod
    def create_edificio(data):
        nuevo_edificio = Edificio(
            nombre=data['nombre'],
            direccion=data['direccion'],
            ubicacion=data.get('ubicacion')
        )
        db.session.add(nuevo_edificio)
        db.session.commit()
        return nuevo_edificio

    @staticmethod
    def update_edificio(edificio_id, data):
        edificio = Edificio.query.get_or_404(edificio_id)
        edificio.nombre = data.get('nombre', edificio.nombre)
        edificio.direccion = data.get('direccion', edificio.direccion)
        edificio.ubicacion = data.get('ubicacion', edificio.ubicacion)
        edificio.estatus = data.get('estatus', edificio.estatus)
        db.session.commit()
        return edificio