from db import db


class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    modelos = db.relationship("Modelo", back_populates="marca")

    def __str__(self) -> str:
        return self.nombre


class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    pais_origen = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean, default=True)  # Añade el atributo activo
    modelos = db.relationship(
        "Modelo", back_populates="fabricante"
    )  # back_populates crea una relacion bidireccional entre Fabricante y Modelo, un fabricante puede tener muchos modelos
    # veo cómo retorno modelos

    def __str__(self) -> str:
        return self.nombre, self.pais_origen


class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fabricante_id = db.Column(
        db.Integer, db.ForeignKey("fabricante.id"), nullable=False
    )  # acá se almacena el id del fabricante, pero no proporciona una representación descriptiva o legible del fabricante
    marca_id = db.Column(
        db.Integer, db.ForeignKey("marca.id"), nullable=False
    )  # Añadido aquí
    activo = db.Column(db.Boolean, default=True)  # Añade el atributo activo
    
    caracteristicas = db.relationship("Caracteristica", back_populates="modelo")
    accesorios = db.relationship("Accesorio", back_populates="modelo")

    fabricante = db.relationship("Fabricante", back_populates="modelos")
    marca = db.relationship("Marca", back_populates="modelos")

    def __str__(self) -> str:
        return self.nombre


class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=True)
    correo_electronico = db.Column(db.String(50), nullable=True)
    activo = db.Column(db.Boolean, default=True)

    def __str__(self) -> str:
        return self.nombre


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    def __str__(self) -> str:
        return self.nombre


class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    peso = db.Column(db.Float, nullable=True)
    resolucion_pantalla = db.Column(db.String(50), nullable=True)
    capacidad_bateria = db.Column(db.Integer, nullable=True)
    sistema_operativo = db.Column(db.String(50), nullable=True)
    precio_lista = db.Column(db.Float, nullable=True)
    camara = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.String(200), nullable=False)
    lanzamiento = db.Column(db.Date, nullable=True)
    activo = db.Column(db.Boolean, default=True)

    modelo = db.relationship("Modelo", back_populates="caracteristicas")

    def __str__(self) -> str:
        return (
            self.peso,
            self.resolucion_pantalla,
            self.capacidad_bateria,
            self.sistema_operativo,
            self.precio_lista,
            self.activo,
            self.camara,
            self.descripcion,
            self.lanzamiento,
        )


class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    cargador = db.Column(db.Boolean, default=True)
    auriculares = db.Column(db.Boolean, default=True)
    chip = db.Column(db.Boolean, default=True)
    funda = db.Column(db.Boolean, default=True)
    activo = db.Column(db.Boolean, default=True)

    modelo = db.relationship("Modelo", back_populates="accesorios")

    def __str__(self) -> str:
        return self.cargador, self.auriculares, self.chip, self.funda


class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey("marca.id"), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"), nullable=False)
    caracteristica_id = db.Column(
        db.Integer, db.ForeignKey("caracteristica.id"), nullable=False
    )
    accesorio_id = db.Column(db.Integer, db.ForeignKey("accesorio.id"), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    categoria = db.relationship("Categoria", backref=db.backref("equipos", lazy=True))
    marca = db.relationship("Marca", backref=db.backref("equipos", lazy=True))
    modelo = db.relationship("Modelo", backref=db.backref("equipos", lazy=True))
    caracteristica = db.relationship(
        "Caracteristica", backref=db.backref("equipos", lazy=True)
    )
    accesorio = db.relationship("Accesorio", backref=db.backref("equipos", lazy=True))

    def __repr__(self):
        return self.id


class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedor.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=True)
    fecha = db.Column(db.Date, nullable=True)

    proveedor = db.relationship(
        "Proveedor", backref=db.backref("inventario", lazy=True)
    )

    def __repr__(self):
        return f"<Inventario {self.id}>"


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    inventario_id = db.Column(
        db.Integer, db.ForeignKey("inventario.id"), nullable=False
    )
    fecha = db.Column(db.Date, nullable=True)

    inventario = db.relationship("Inventario", backref=db.backref("cliente", lazy=True))

    def __repr__(self):
        return self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean(0))
