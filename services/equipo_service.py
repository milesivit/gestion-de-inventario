from repositories.equipo_repository import EquipoRepository

class EquipoService:
    def __init__(self):
        self.repository = EquipoRepository()  # Instancia del repositorio

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def create(self, categoria_id, marca_id, modelo_id, caracteristica_id, accesorio_id):
        return self.repository.create(categoria_id, marca_id, modelo_id, caracteristica_id, accesorio_id)

    def update(self, equipo):
        return self.repository.update(equipo)

    def hide_by_id(self, id):
        return self.repository.hide_by_id(id)
