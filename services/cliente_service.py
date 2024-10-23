from repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()  # Instanciar el repositorio

    def get_all(self):
        return self.repository.get_all()

    def create(self, nombre, dni, inventario_id, fecha):
        return self.repository.create(nombre, dni, inventario_id, fecha)

    def update(self, id, nombre, dni, inventario_id, fecha):
        return self.repository.update(id, nombre, dni, inventario_id, fecha)

    def delete_by_id(self, id):
        return self.repository.delete_by_id(id)

    def get_by_id(self, id):
        return self.repository.get_by_id(id)
