from app import db
from models import Marca, Categoria, Modelo, Proveedor, Accesorio, Fabricante, Caracteristica, Equipo

class RestaurarService:
    def restaurar_entidad(self, modelo, entidad_id):
        entidad = modelo.query.get(entidad_id)
        if entidad and not entidad.activo:
            entidad.activo = True
            db.session.commit()
            return True
        return False

    def obtener_inactivos(self, modelo):
        return modelo.query.filter_by(activo=False).all()
