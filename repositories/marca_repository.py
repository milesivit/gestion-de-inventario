from app import db
from models import Marca


class MarcaRepository:
    """
    Clase encargada de manejar las operaciones de base de datos para la entidad Marca.
    """

    def get_all(self):
        return Marca.query.all()

    def get_active(self):
        return Marca.query.filter_by(
            activo=True
        ).all()  # Filtra solo las marcas activas

    def get_by_id(self, id):
        return Marca.query.get(id)

    def exists_by_name(self, nombre):
        return Marca.query.filter_by(nombre=nombre).first() is not None

    def create(self, nombre):
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        return nueva_marca

    def hide_by_id(self, id):
        marca = Marca.query.get(id)
        if marca:
            marca.activo = False  # Ocultar la marca
            db.session.commit()
            return True
        return False

    def update(self, id, nombre):
        marca = Marca.query.get(id)
        if marca:
            marca.nombre = nombre
            db.session.commit()
            return marca
        return None
