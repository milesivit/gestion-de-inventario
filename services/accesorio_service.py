from repositories.accesorio_repository import AccesorioRepository


class AccesorioService:

    def __init__(self):
        self.repository = AccesorioRepository()  # Instancia del repositorio

    def get_active(self):
        return self.repository.get_active()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def exists_for_modelo(self, modelo_id):
        return self.repository.exists_for_modelo(modelo_id)

    def create(self, modelo_id, cargador, auriculares, chip, funda, activo):
        return self.repository.create(
            modelo_id, cargador, auriculares, chip, funda, activo
        )

    def update(self, id, modelo_id, cargador, auriculares, chip, funda):
        return self.repository.update(id, modelo_id, cargador, auriculares, chip, funda)

    def hide_by_id(self, id):
        return self.repository.hide_by_id(id)
