from db import ma
from marshmallow import validates, ValidationError, fields

from models import (
    User,
    Marca,
    Fabricante,
    Modelo,
    Caracteristica,
    Categoria,
    Accesorio,
    Equipo,
    Proveedor,
    Cliente,
    Inventario,
)

# Esquema para el modelo User
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()  # Campo id del usuario
    username = ma.auto_field()  # Campo username del usuario
    password_hash = ma.auto_field()  # Campo hash de la contraseña del usuario
    is_admin = ma.auto_field()  # Campo booleano para identificar si es admin

    # Validación para el campo username
    @validates("username")
    def validate_username(self, value):
        # Verifica si el nombre de usuario ya existe
        user = User.query.filter_by(username=value).first()
        if user:
            # Levanta un error si el nombre de usuario ya está en uso
            raise ValidationError("Ya existe un usuario con ese username.")
        return value


# Esquema minimalista para el modelo User
class UserMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()  # Solo incluye el campo username


# Esquema para el modelo Marca
class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    id = ma.auto_field()  # Campo id de la marca
    nombre = ma.auto_field()  # Nombre de la marca
    activo = ma.auto_field()  # Estado de la marca (activo/inactivo)


# Esquema minimalista para el modelo Marca
class MarcaMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    nombre = ma.auto_field()  # Solo incluye el nombre de la marca


# Esquema para el modelo Fabricante
class FabricanteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabricante

    id = ma.auto_field()  # Campo id del fabricante
    nombre = ma.auto_field()  # Nombre del fabricante
    pais_origen = ma.auto_field()  # País de origen del fabricante
    activo = ma.auto_field()  # Estado del fabricante (activo/inactivo)


# Esquema minimalista para el modelo Fabricante
class FabricanteMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Fabricante

    nombre = ma.auto_field()  # Solo incluye el nombre del fabricante


# Esquema para el modelo Modelo, incluyendo marca y fabricante anidados
class ModeloSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo

    id = ma.auto_field()  # Campo id del modelo
    nombre = ma.auto_field()  # Nombre del modelo
    activo = ma.auto_field()  # Estado del modelo (activo/inactivo)

    fabricante = fields.Nested(FabricanteSchema)  # Objeto fabricante anidado
    marca = fields.Nested(MarcaSchema)  # Objeto marca anidado


# Esquema minimalista para el modelo Modelo
class ModeloMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo

    nombre = ma.auto_field()  # Solo incluye el nombre del modelo


# Esquema para el modelo Caracteristica
class CaracteristicaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caracteristica

    # Campos del modelo Caracteristica
    id = ma.auto_field()
    modelo_id = ma.auto_field()
    peso = ma.auto_field()
    resolucion_pantalla = ma.auto_field()
    capacidad_bateria = ma.auto_field()
    sistema_operativo = ma.auto_field()
    precio_lista = ma.auto_field()
    camara = ma.auto_field()
    descripcion = ma.auto_field()
    lanzamiento = ma.auto_field()
    activo = ma.auto_field()

    modelo = fields.Nested(ModeloSchema)  # Objeto modelo anidado


# Esquema minimalista para el modelo Caracteristica
class CaracteristicaMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caracteristica

    # Campos del modelo Caracteristica en forma minimalista
    peso = ma.auto_field()
    resolucion_pantalla = ma.auto_field()
    capacidad_bateria = ma.auto_field()
    sistema_operativo = ma.auto_field()
    camara = ma.auto_field()
    descripcion = ma.auto_field()
    lanzamiento = ma.auto_field()


# Esquema para el modelo Categoria
class CategoriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria

    id = ma.auto_field()  # Campo id de la categoría
    nombre = ma.auto_field()  # Nombre de la categoría
    activo = ma.auto_field()  # Estado de la categoría


# Esquema minimalista para el modelo Categoria
class CategoriaMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria

    nombre = ma.auto_field()  # Solo incluye el nombre de la categoría


# Esquema para el modelo Accesorio
class AcessorioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorio

    # Campos del modelo Accesorio
    id = ma.auto_field()
    modelo_id = ma.auto_field()
    cargador = ma.auto_field()
    auriculares = ma.auto_field()
    chip = ma.auto_field()
    funda = ma.auto_field()
    activo = ma.auto_field()

    modelo = fields.Nested(ModeloSchema)  # Objeto modelo anidado


# Esquema minimalista para el modelo Accesorio
class AcessorioMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorio

    # Campos de accesorio en forma minimalista
    cargador = ma.auto_field()
    auriculares = ma.auto_field()
    chip = ma.auto_field()
    funda = ma.auto_field()


# Esquema para el modelo Equipo
class EquipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo

    # Campos del modelo Equipo
    categoria_id = ma.auto_field()
    marca_id = ma.auto_field()
    modelo_id = ma.auto_field()
    caracteristica_id = ma.auto_field()
    accesorio_id = ma.auto_field()

    # Objetos anidados
    categoria = fields.Nested(CategoriaSchema)
    marca = fields.Nested(MarcaSchema)
    modelo = fields.Nested(ModeloSchema)
    caracteristica = fields.Nested(CaracteristicaSchema)
    accesorio = fields.Nested(AcessorioSchema)


# Esquema minimalista para el modelo Equipo
class EquipoMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo

    # Campos minimalistas de Equipo
    categoria_id = ma.auto_field()
    marca_id = ma.auto_field()
    modelo_id = ma.auto_field()
    caracteristica_id = ma.auto_field()
    accesorio_id = ma.auto_field()


# Esquema para el modelo Proveedor
class ProveedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    # Campos del modelo Proveedor
    id = ma.auto_field()
    nombre = ma.auto_field()
    telefono = ma.auto_field()
    direccion = ma.auto_field()
    correo_electronico = ma.auto_field()
    activo = ma.auto_field()


# Esquema minimalista para el modelo Proveedor
class ProveedorMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    # Campos minimalistas del proveedor
    nombre = ma.auto_field()
    correo_electronico = ma.auto_field()


# Esquema para el modelo Inventario
class InventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventario

    # Campos del modelo Inventario
    id = ma.auto_field()
    nombre = ma.auto_field()
    proveedor_id = ma.auto_field()
    cantidad = ma.auto_field()
    fecha = ma.auto_field()

    proveedor = fields.Nested(ProveedorSchema)  # Proveedor anidado


# Esquema minimalista para el modelo Inventario
class InventarioMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventario

    # Campos minimalistas del inventario
    nombre = ma.auto_field()
    proveedor_id = ma.auto_field()
    cantidad = ma.auto_field()


# Esquema para el modelo Cliente
class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente

    # Campos del modelo Cliente
    id = ma.auto_field()
    nombre = ma.auto_field()
    dni = ma.auto_field()
    inventario_id = ma.auto_field()
    fecha = ma.auto_field()

    inventario = fields.Nested(InventarioSchema)  # Inventario anidado


# Esquema minimalista para el modelo Cliente
class ClienteMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente

    nombre = ma.auto_field()  # Solo incluye el nombre del cliente
