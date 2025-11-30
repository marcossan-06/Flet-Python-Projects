class Vehiculo:
    def __init__(self, matricula: str, propietario: str, tipo_vehiculo: str):
        self.matricula = matricula.upper()
        self.propietario = propietario
        self.tipo_vehiculo = tipo_vehiculo