from app import db
from models import Inventario, Modelo, Proveedor

class InventarioRepository:
    def get_all(self):
        return Inventario.query.all()

    def create(self, nombre, proveedor_id, cantidad, fecha):
        nuevo_inventario = Inventario(
            nombre=nombre,
            proveedor_id=proveedor_id,
            cantidad=cantidad,
            fecha=fecha,
        )
        db.session.add(nuevo_inventario)
        db.session.commit()
        return nuevo_inventario

    def update(self, id, nombre, proveedor_id, cantidad, fecha):
        inventario = Inventario.query.get(id)
        if inventario:
            inventario.nombre = nombre
            inventario.proveedor_id = proveedor_id
            inventario.cantidad = cantidad
            inventario.fecha = fecha
            db.session.commit()
            return inventario
        return None

    def delete_by_id(self, id):
        inventario = Inventario.query.get(id)
        if inventario:
            db.session.delete(inventario)
            db.session.commit()
            return True
        return False

    def get_by_id(self, id):
        return Inventario.query.get(id)

    def get_modelos(self):
        return Modelo.query.filter_by(activo=True).all()  # Obtener modelos activos

    def get_proveedores(self):
        return Proveedor.query.filter_by(activo=True).all()  # Obtener proveedores activos
