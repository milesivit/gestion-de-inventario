from repositories.caracteristica_repository import CaracteristicaRepository

class CaracteristicaService:
    def __init__(self):
        self.repository = CaracteristicaRepository()  # Instancia del repositorio

    def get_all(self):
        return self.repository.get_all()
    
    def get_active(self):
        return self.repository.get_active()
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, modelo_id, peso, resolucion_pantalla, capacidad_bateria, sistema_operativo, precio_lista, camara, descripcion, lanzamiento):
        return self.repository.create(
            modelo_id=modelo_id,
            peso=peso,
            resolucion_pantalla=resolucion_pantalla,
            capacidad_bateria=capacidad_bateria,
            sistema_operativo=sistema_operativo,
            precio_lista=precio_lista,
            camara=camara,
            descripcion=descripcion,
            lanzamiento=lanzamiento
        )
    
    def hide_by_id(self, id):
        return self.repository.hide_by_id(id)

    def update(self, id, modelo_id, peso, resolucion_pantalla, capacidad_bateria, sistema_operativo, precio_lista, camara, descripcion, lanzamiento):
        return self.repository.update(
            id=id,
            modelo_id=modelo_id,
            peso=peso,
            resolucion_pantalla=resolucion_pantalla,
            capacidad_bateria=capacidad_bateria,
            sistema_operativo=sistema_operativo,
            precio_lista=precio_lista,
            camara=camara,
            descripcion=descripcion,
            lanzamiento=lanzamiento
        )
    
    def get_active_models(self):
        from models import Modelo
        return Modelo.query.filter_by(activo=True).all()  # Obtener modelos activos
