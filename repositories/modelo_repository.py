from app import db
from models import Modelo, Fabricante, Marca

class ModeloRepository:
    """
    Clase encargada de manejar las operaciones de base de datos para la entidad Modelo.
    """

    def get_all(self):
        return Modelo.query.all()

    def get_active(self):
        return Modelo.query.filter_by(activo=True).all()  # Filtrar solo modelos activos

    def get_by_id(self, id):
        return Modelo.query.get(id)

    def get_fabricante_choices(self):
        return [(fabricante.id, fabricante.nombre) for fabricante in Fabricante.query.all()]  # Obtener opciones de fabricantes

    def get_marca_choices(self):
        return [(m.id, m.nombre) for m in Marca.query.filter_by(activo=True).all()]  # Obtener opciones de marcas activas

    def create(self, nombre, fabricante_id, marca_id):
        nuevo_modelo = Modelo(
            nombre=nombre,
            fabricante_id=fabricante_id,
            marca_id=marca_id
        )
        db.session.add(nuevo_modelo)
        db.session.commit()
        return nuevo_modelo

    def hide_by_id(self, id):
        modelo = Modelo.query.get(id)
        if modelo:
            modelo.activo = False  # Ocultar el modelo
            db.session.commit()
            return True
        return False

    def update(self, id, nombre, fabricante_id, marca_id):
        modelo = Modelo.query.get(id)
        if modelo:
            modelo.nombre = nombre
            modelo.fabricante_id = fabricante_id
            modelo.marca_id = marca_id
            db.session.commit()
            return modelo
        return None
