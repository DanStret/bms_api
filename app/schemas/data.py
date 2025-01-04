from app import ma
from app.models.data import DataCO2, DataPresurizacion

class DataCO2Schema(ma.SQLAlchemySchema):
    class Meta:
        model = DataCO2

    id = ma.auto_field()
    id_sistema = ma.auto_field()
    timestamp = ma.auto_field()
    concentracion_co2 = ma.auto_field()
    presion = ma.auto_field()
    temperatura = ma.auto_field()
    flujo_aire = ma.auto_field()

class DataPresurizacionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DataPresurizacion

    id = ma.auto_field()
    id_sistema = ma.auto_field()
    timestamp = ma.auto_field()
    tensionMotor = ma.auto_field()
    tensionDC = ma.auto_field()
    corriente = ma.auto_field()
    potencia = ma.auto_field()
    frecuencia = ma.auto_field()
    temperatura = ma.auto_field()
    IA = ma.auto_field()
    AV = ma.auto_field()

# Instancias de schemas
data_co2_schema = DataCO2Schema()
data_co2s_schema = DataCO2Schema(many=True)
data_presurizacion_schema = DataPresurizacionSchema()
data_presurizacions_schema = DataPresurizacionSchema(many=True)