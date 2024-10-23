from repositories.proveedor_repository import ProveedorRepository

class ProveedorService:
    """
    Clase que encapsula la lógica de negocio relacionada con los proveedores.
    """

    def __init__(self):
        self.repository = ProveedorRepository()  # Instancia del repositorio

    def get_all(self):
        return self.repository.get_all()
    
    def get_active(self):
        return self.repository.get_active()
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def exists_by_name(self, nombre):
        return self.repository.exists_by_name(nombre)
    
    def create(self, nombre, telefono, direccion, correo_electronico):
        return self.repository.create(nombre, telefono, direccion, correo_electronico)
    
    def hide_by_id(self, id):
        return self.repository.hide_by_id(id)
    
    def update(self, id, nombre, telefono, direccion, correo_electronico):
        return self.repository.update(id, nombre, telefono, direccion, correo_electronico)
