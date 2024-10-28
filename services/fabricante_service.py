from repositories.fabricante_repository import FabricanteRepository


class FabricanteService:
    """
    Clase que encapsula la lógica de negocio relacionada con los fabricantes.
    """

    def __init__(self):
        self.repository = FabricanteRepository()  # Instancia del repositorio

    def get_all(self):
        return self.repository.get_all()

    def get_active(self):
        return self.repository.get_active()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def fabricante_exists(self, nombre):
        return self.repository.fabricante_exists(nombre)

    def create(self, nombre, pais_origen):
        return self.repository.create(nombre, pais_origen)

    def hide_by_id(self, id):
        return self.repository.hide_by_id(id)

    def update(self, id, nombre, pais_origen):
        return self.repository.update(id, nombre, pais_origen)
