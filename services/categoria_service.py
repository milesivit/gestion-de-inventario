from repositories.categoria_repository import CategoriaRepository

class CategoriaService:

    def __init__(self):
        self.repository = CategoriaRepository()  # Instancia del repositorio

    def get_all(self):
        return self.repository.get_all()
    
    def get_active(self):
        return self.repository.get_active()
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def exists_by_name(self, nombre):
        return self.repository.exists_by_name(nombre)
    
    def create(self, nombre):
        return self.repository.create(nombre)
    
    def hide_by_id(self, id):
        return self.repository.hide_by_id(id)
    
    def update(self, id, nombre):
        return self.repository.update(id, nombre)
