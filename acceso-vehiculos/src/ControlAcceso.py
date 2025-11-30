import json
from datetime import datetime

from Vehiculo import Vehiculo


class ControlAcceso:
    def __init__(self):
        self.archivo_json = "accesos.json"
        self.vehiculos_autorizados = {}
        self.registro_accesos = []
        self.leer_json()

    def leer_json(self):
        try:
            with open(self.archivo_json) as json_file:
                data = json.load(json_file)
                self.vehiculos_autorizados = data.get("VEHICULOS_AUTORIZADOS", {})
                self.registro_accesos = data.get("REGISTRO_ACCESOS", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.vehiculos_autorizados = {}
            self.registro_accesos = []

    def escribir_json(self):
        data = {
            "VEHICULOS_AUTORIZADOS": self.vehiculos_autorizados,
            "REGISTRO_ACCESOS": self.registro_accesos
        }

        with open(self.archivo_json, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def comprobar(self, matricula: str) -> bool:
        return matricula.upper() in self.vehiculos_autorizados

    def add_vehiculo(self, vehiculo: Vehiculo) -> bool:
        if self.comprobar(vehiculo.matricula):
            return False
        self.vehiculos_autorizados[vehiculo.matricula] = {
            "propietario": vehiculo.propietario,
            "tipo_vehiculo": vehiculo.tipo_vehiculo,
        }
        self.escribir_json()
        return True

    def add_registro(self, matricula: str, resultado: str):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registro_accesos.insert(0, {
            "fecha_hora": fecha,
            "matricula": matricula.upper(),
            "resultado": resultado,
        })
        self.escribir_json()