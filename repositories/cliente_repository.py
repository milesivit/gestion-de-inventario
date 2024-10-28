from app import db
from models import Cliente


class ClienteRepository:
    def get_all(self):
        return Cliente.query.all()

    def create(self, nombre, dni, inventario_id, fecha):
        nuevo_cliente = Cliente(
            nombre=nombre,
            dni=dni,
            inventario_id=inventario_id,
            fecha=fecha,
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return nuevo_cliente

    def update(self, id, nombre, dni, inventario_id, fecha):
        cliente = Cliente.query.get(id)
        if cliente:
            cliente.nombre = nombre
            cliente.dni = dni
            cliente.inventario_id = inventario_id
            cliente.fecha = fecha
            db.session.commit()
            return cliente
        return None

    def delete_by_id(self, id):
        cliente = Cliente.query.get(id)
        if cliente:
            db.session.delete(cliente)
            db.session.commit()
            return True
        return False

    def get_by_id(self, id):
        return Cliente.query.get(id)
