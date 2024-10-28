from app import db
from models import Categoria


class CategoriaRepository:
    """
    Clase encargada de manejar las operaciones de base de datos para la entidad Categoria.
    """

    def get_all(self):
        return Categoria.query.all()

    def get_active(self):
        return Categoria.query.filter_by(
            activo=True
        ).all()  # Filtra solo las categorías activas

    def get_by_id(self, id):
        return Categoria.query.get(id)

    def exists_by_name(self, nombre):
        return Categoria.query.filter_by(nombre=nombre).first() is not None

    def create(self, nombre):
        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        return nueva_categoria

    def hide_by_id(self, id):
        categoria = Categoria.query.get(id)
        if categoria:
            categoria.activo = False  # Ocultar la categoría
            db.session.commit()
            return True
        return False

    def update(self, id, nombre):
        categoria = Categoria.query.get(id)
        if categoria:
            categoria.nombre = nombre
            db.session.commit()
            return categoria
        return None
