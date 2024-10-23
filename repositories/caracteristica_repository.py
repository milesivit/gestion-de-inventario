from app import db
from models import Caracteristica

class CaracteristicaRepository:
    """
    Clase encargada de manejar las operaciones de base de datos para la entidad Caracteristica.
    """

    def get_all(self):
        return Caracteristica.query.all()
    
    def get_active(self):
        return Caracteristica.query.filter_by(activo=True).all()  # Filtra solo las características activas
    
    def get_by_id(self, id):
        return Caracteristica.query.get(id)
    
    def create(self, modelo_id, peso, resolucion_pantalla, capacidad_bateria, sistema_operativo, precio_lista, camara, descripcion, lanzamiento):
        nueva_caracteristica = Caracteristica(
            modelo_id=modelo_id,
            peso=peso,
            resolucion_pantalla=resolucion_pantalla,
            capacidad_bateria=capacidad_bateria,
            sistema_operativo=sistema_operativo,
            precio_lista=precio_lista,
            camara=camara,
            descripcion=descripcion,
            lanzamiento=lanzamiento,
            activo=True
        )
        db.session.add(nueva_caracteristica)
        db.session.commit()
        return nueva_caracteristica
    
    def hide_by_id(self, id):
        caracteristica = Caracteristica.query.get(id)
        if caracteristica:
            caracteristica.activo = False  # Ocultar la característica
            db.session.commit()
            return True
        return False
    
    def update(self, id, modelo_id, peso, resolucion_pantalla, capacidad_bateria, sistema_operativo, precio_lista, camara, descripcion, lanzamiento):
        caracteristica = Caracteristica.query.get(id)
        if caracteristica:
            caracteristica.modelo_id = modelo_id
            caracteristica.peso = peso
            caracteristica.resolucion_pantalla = resolucion_pantalla
            caracteristica.capacidad_bateria = capacidad_bateria
            caracteristica.sistema_operativo = sistema_operativo
            caracteristica.precio_lista = precio_lista
            caracteristica.camara = camara
            caracteristica.descripcion = descripcion
            caracteristica.lanzamiento = lanzamiento
            db.session.commit()
            return caracteristica
        return None
