from app import db
from models import Accesorio


class AccesorioRepository:
    """
    Clase encargada de manejar las operaciones de base de datos para la entidad Accesorio.
    """

    def get_active(self):
        return Accesorio.query.filter_by(
            activo=True
        ).all()  # Filtra solo los accesorios activos

    def get_by_id(self, id):
        return Accesorio.query.get(id)

    def exists_for_modelo(self, modelo_id):
        return Accesorio.query.filter_by(modelo_id=modelo_id).first() is not None

    def create(self, modelo_id, cargador, auriculares, chip, funda, activo):
        nuevo_accesorio = Accesorio(
            modelo_id=modelo_id,
            cargador=cargador,
            auriculares=auriculares,
            chip=chip,
            funda=funda,
            activo=activo,
        )
        db.session.add(nuevo_accesorio)
        db.session.commit()
        return nuevo_accesorio

    def update(self, id, modelo_id, cargador, auriculares, chip, funda):
        accesorio = Accesorio.query.get(id)
        if accesorio:
            accesorio.modelo_id = modelo_id
            accesorio.cargador = cargador
            accesorio.auriculares = auriculares
            accesorio.chip = chip
            accesorio.funda = funda
            db.session.commit()
            return accesorio
        return None

    def hide_by_id(self, id):
        accesorio = Accesorio.query.get(id)
        if accesorio:
            accesorio.activo = False  # Ocultar el accesorio
            db.session.commit()
            return True
        return False
