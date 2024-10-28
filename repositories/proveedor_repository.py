from app import db
from models import Proveedor


class ProveedorRepository:
    """
    Clase encargada de manejar las operaciones de base de datos para la entidad Proveedor.
    """

    def get_all(self):
        return Proveedor.query.all()

    def get_active(self):
        return Proveedor.query.filter_by(
            activo=True
        ).all()  # Filtrar solo proveedores activos

    def get_by_id(self, id):
        return Proveedor.query.get(id)

    def exists_by_name(self, nombre):
        return Proveedor.query.filter_by(nombre=nombre).first() is not None

    def create(self, nombre, telefono, direccion, correo_electronico):
        nuevo_proveedor = Proveedor(
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            correo_electronico=correo_electronico,
        )
        db.session.add(nuevo_proveedor)
        db.session.commit()
        return nuevo_proveedor

    def hide_by_id(self, id):
        proveedor = Proveedor.query.get(id)
        if proveedor:
            proveedor.activo = False  # Ocultar el proveedor
            db.session.commit()
            return True
        return False

    def update(self, id, nombre, telefono, direccion, correo_electronico):
        proveedor = Proveedor.query.get(id)
        if proveedor:
            proveedor.nombre = nombre
            proveedor.telefono = telefono
            proveedor.direccion = direccion
            proveedor.correo_electronico = correo_electronico
            db.session.commit()
            return proveedor
        return None
