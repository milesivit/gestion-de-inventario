from app import db
from models import Fabricante

class FabricanteRepository:
    """
    Clase que maneja las operaciones de base de datos para la entidad Fabricante.
    """

    def get_all(self):
        return Fabricante.query.all()

    def get_active(self):
        return Fabricante.query.filter_by(activo=True).all()  # Solo los fabricantes activos

    def get_by_id(self, id):
        return Fabricante.query.get(id)

    def create(self, nombre, pais_origen):
        nuevo_fabricante = Fabricante(nombre=nombre, pais_origen=pais_origen)
        db.session.add(nuevo_fabricante)
        db.session.commit()
        return nuevo_fabricante

    def fabricante_exists(self, nombre):
        return Fabricante.query.filter_by(nombre=nombre).first() is not None

    def hide_by_id(self, id):
        fabricante = Fabricante.query.get(id)
        if fabricante:
            fabricante.activo = False  # Ocultar fabricante
            db.session.commit()
            return True
        return False

    def update(self, id, nombre, pais_origen):
        fabricante = Fabricante.query.get(id)
        if fabricante:
            fabricante.nombre = nombre
            fabricante.pais_origen = pais_origen
            db.session.commit()
            return fabricante
        return None
