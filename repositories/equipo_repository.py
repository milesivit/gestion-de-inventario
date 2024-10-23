from app import db
from models import Equipo

class EquipoRepository:
    """
    Clase encargada de manejar las operaciones de base de datos para la entidad Equipo.
    """

    def get_all(self):
        return Equipo.query.filter_by(activo=True).all()  # Obtener solo equipos activos

    def get_by_id(self, id):
        return Equipo.query.get(id)

    def create(self, categoria_id, marca_id, modelo_id, caracteristica_id, accesorio_id):
        nuevo_equipo = Equipo(
            categoria_id=categoria_id,
            marca_id=marca_id,
            modelo_id=modelo_id,
            caracteristica_id=caracteristica_id,
            accesorio_id=accesorio_id,
        )
        db.session.add(nuevo_equipo)
        db.session.commit()
        return nuevo_equipo

    def update(self, equipo):
        db.session.commit()  # Solo necesitamos hacer commit al actualizar

    def hide_by_id(self, id):
        equipo = Equipo.query.get(id)
        if equipo:
            equipo.activo = False  # Ocultar el equipo
            db.session.commit()
            return True
        return False
