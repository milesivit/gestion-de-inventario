from repositories.inventario_repository import InventarioRepository

class InventarioService:
    def __init__(self):
        self.repository = InventarioRepository()  # Instanciar el repositorio

    def get_all(self):
        return self.repository.get_all()

    def create(self, nombre, proveedor_id, cantidad, fecha):
        return self.repository.create(nombre, proveedor_id, cantidad, fecha)

    def update(self, id, nombre, proveedor_id, cantidad, fecha):
        return self.repository.update(id, nombre, proveedor_id, cantidad, fecha)

    def delete_by_id(self, id):
        return self.repository.delete_by_id(id)

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_modelos(self):
        return self.repository.get_modelos()  # Método para obtener modelos activos

    def get_proveedores(self):
        return self.repository.get_proveedores()  # Método para obtener proveedores activos
