from repositories.modelo_repository import ModeloRepository


class ModeloService:
    """
    Clase que encapsula la lógica de negocio relacionada con los modelos.
    """

    def __init__(self):
        self.repository = ModeloRepository()  # Instancia del repositorio

    def get_all(self):
        return self.repository.get_all()

    def get_active(self):
        return self.repository.get_active()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_fabricante_choices(self):
        return self.repository.get_fabricante_choices()

    def get_marca_choices(self):
        return self.repository.get_marca_choices()

    def create(self, nombre, fabricante_id, marca_id):
        return self.repository.create(nombre, fabricante_id, marca_id)

    def hide_by_id(self, id):
        return self.repository.hide_by_id(id)

    def update(self, id, nombre, fabricante_id, marca_id):
        return self.repository.update(id, nombre, fabricante_id, marca_id)
