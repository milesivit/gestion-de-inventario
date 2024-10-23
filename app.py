import os
from db import db

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_migrate import Migrate

from flask_jwt_extended import (
    JWTManager,
)

app = Flask(__name__)

from views import register_bp

register_bp(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI"
)  # esto se conecta al .env
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# esto sirve para flaskWTF
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from dotenv import load_dotenv
from models import (
    Marca,
    Proveedor,
    Modelo,
    Fabricante,
    Categoria,
    Caracteristica,
    Accesorio,
    Equipo,
    Inventario,
    Cliente,
)
from forms import (
    MarcaForm,
    ProveedorForm,
    EmptyForm,
    FabricanteForm,
    ModeloForm,
    CategoriaForm,
    CaracteristicaForm,
    AccesorioForm,
    EquipoForm,
)
from services.marca_service import MarcaService
from services.proveedor_service import ProveedorService
from services.modelo_service import ModeloService
from services.fabricante_service import FabricanteService
from services.restaurar_service import RestaurarService
from services.categoria_service import CategoriaService
from services.caracteristica_service import CaracteristicaService
from services.accesorio_service import AccesorioService
from services.equipo_service import EquipoService
from services.cliente_service import ClienteService


load_dotenv()


# -----------------------------------------------------------------------------------------------------------------
@app.route("/")  # página principal
def index():
    return render_template("index.html")


# -----------------------------------------------------------------------------------------------------------------
@app.route("/marcas")
def marcas():
    services = MarcaService()  # No pasar MarcaRepository aquí
    marcas = services.get_all()  # Llama al método get_all
    return render_template("marcas.html", marcas=marcas)


# Ruta para agregar nuevas marcas
@app.route("/agregar-marcas", methods=["GET", "POST"])
def agregar_marcas():
    form = MarcaForm()
    services = MarcaService()  # Instanciar el servicio
    if form.validate_on_submit():  # Validar el formulario
        if services.exists_by_name(form.nombre.data):  # Verificar si ya existe la marca
            form.nombre.errors.append("Esta marca ya existe.")
        else:
            services.create(form.nombre.data)  # Crear nueva marca usando el servicio
            return redirect(url_for("marcas"))  # Redirigir a la página de marcas
    return render_template("agregar_marcas.html", form=form)


# Ruta para eliminar marcas (ocultarlas)
@app.route("/eliminar-marcas", methods=["GET", "POST"])
def eliminar_marcas():
    form = MarcaForm()
    services = MarcaService()  # Instanciar el servicio
    if request.method == "POST":
        marca_id = request.form.get("marca_id")
        if services.hide_by_id(marca_id):  # Ocultar marca usando el servicio
            return redirect(url_for("eliminar_marcas"))
        else:
            form.errors["marca_id"] = ["Marca no encontrada."]
    marcas = services.get_active()  # Obtener solo las marcas activas
    return render_template("eliminar_marcas.html", marcas=marcas, form=form)


# Ruta para modificar una marca existente
@app.route("/modificar-marcas/<int:id>", methods=["GET", "POST"])
def modificar_marcas(id):
    services = MarcaService()  # Instanciar el servicio
    marca = services.get_by_id(id)  # Obtener marca por ID
    form = MarcaForm(obj=marca)
    if form.validate_on_submit():
        if (
            services.exists_by_name(form.nombre.data)
            and marca.nombre != form.nombre.data
        ):
            form.nombre.errors.append("Esta marca ya existe.")
        else:
            services.update(
                id, form.nombre.data
            )  # Actualizar la marca usando el servicio
            return redirect(url_for("marcas"))
    form.submit.label.text = "Guardar Cambios"
    return render_template("modificar_marcas.html", form=form, marca=marca)


# -----------------------------------------------------------------------------------------------------------------
# Ruta para mostrar todos los proveedores
@app.route("/proveedores")
def proveedores():
    services = ProveedorService()  # Instanciar el servicio
    proveedores = services.get_all()  # Llamar al método get_all del servicio
    return render_template("proveedores.html", proveedores=proveedores)


# Ruta para agregar un nuevo proveedor
@app.route("/agregar-proveedor", methods=["GET", "POST"])
def agregar_proveedor():
    form = ProveedorForm()
    services = ProveedorService()  # Instanciar el servicio
    if form.validate_on_submit():  # Validar el formulario
        if services.exists_by_name(
            form.nombre.data
        ):  # Verificar si ya existe el proveedor
            form.nombre.errors.append("Este proveedor ya existe.")
        else:
            services.create(
                form.nombre.data,
                form.telefono.data,
                form.direccion.data,
                form.correo_electronico.data,
            )
            return redirect(
                url_for("proveedores")
            )  # Redirigir a la página de proveedores
    return render_template("agregar_proveedor.html", form=form)


# Ruta para eliminar (ocultar) un proveedor
@app.route("/eliminar-proveedor", methods=["GET", "POST"])
def eliminar_proveedor():
    form = ProveedorForm()
    services = ProveedorService()  # Instanciar el servicio
    if request.method == "POST":
        proveedor_id = request.form.get("proveedor_id")
        if services.hide_by_id(proveedor_id):  # Ocultar proveedor
            return redirect(url_for("eliminar_proveedor"))
        else:
            form.errors["proveedor_id"] = ["Proveedor no encontrado."]

    proveedores = services.get_active()  # Obtener solo los proveedores activos
    return render_template(
        "eliminar_proveedor.html", proveedores=proveedores, form=form
    )


# Ruta para modificar un proveedor existente
@app.route("/modificar-proveedor/<int:id>", methods=["GET", "POST"])
def modificar_proveedor(id):
    services = ProveedorService()  # Instanciar el servicio
    proveedor = services.get_by_id(id)  # Obtener proveedor por ID
    form = ProveedorForm(obj=proveedor)

    if form.validate_on_submit():
        services.update(
            id,
            form.nombre.data,
            form.telefono.data,
            form.direccion.data,
            form.correo_electronico.data,
        )
        return redirect(url_for("proveedores"))

    form.submit.label.text = "Guardar cambios"
    return render_template("modificar_proveedor.html", form=form, proveedor=proveedor)


# -----------------------------------------------------------------------------------------------------------------
# Ruta para mostrar todos los modelos activos
@app.route("/modelos")
def modelos():
    services = ModeloService()  # Instanciar el servicio
    modelos = services.get_active()  # Llamar al método get_active del servicio
    return render_template("modelos.html", modelos=modelos)


# Ruta para eliminar (ocultar) un modelo
@app.route("/eliminar-modelo", methods=["GET", "POST"])
def eliminar_modelo():
    form = ModeloForm()
    services = ModeloService()  # Instanciar el servicio

    if request.method == "POST":
        modelo_id = request.form.get("modelo_id")
        if services.hide_by_id(modelo_id):  # Ocultar modelo
            return redirect(url_for("eliminar_modelo"))
        else:
            form.errors["modelo_id"] = ["Modelo no encontrado."]

    modelos = services.get_active()  # Obtener modelos activos
    return render_template("eliminar_modelo.html", modelos=modelos, form=form)


# Ruta para modificar un modelo existente
@app.route("/modificar-modelo/<int:id>", methods=["GET", "POST"])
def modificar_modelo(id):
    services = ModeloService()  # Instanciar el servicio
    modelo = services.get_by_id(id)  # Obtener modelo por ID
    form = ModeloForm(obj=modelo)

    # Cargar los fabricantes y marcas en el formulario
    form.fabricante_id.choices = services.get_fabricante_choices()
    form.marca_id.choices = services.get_marca_choices()

    if form.validate_on_submit():
        services.update(
            id, form.nombre.data, form.fabricante_id.data, form.marca_id.data
        )
        return redirect(url_for("modelos"))

    return render_template("modificar_modelo.html", form=form, modelo=modelo)


# Ruta para agregar un nuevo modelo
@app.route("/agregar-modelo", methods=["GET", "POST"])
def agregar_modelo():
    form = ModeloForm()
    services = ModeloService()  # Instanciar el servicio

    # Cargar los fabricantes y marcas en el formulario
    form.fabricante_id.choices = services.get_fabricante_choices()
    form.marca_id.choices = services.get_marca_choices()

    if form.validate_on_submit():
        services.create(form.nombre.data, form.fabricante_id.data, form.marca_id.data)
        return redirect(url_for("modelos"))

    return render_template("agregar_modelo.html", form=form)


# -----------------------------------------------------------------------------------------------------------------
# Ruta para mostrar todos los fabricantes activos
@app.route("/fabricantes")
def fabricantes():
    service = FabricanteService()  # Instancia del servicio
    fabricantes = service.get_active()  # Obtener fabricantes activos
    return render_template("fabricantes.html", fabricantes=fabricantes)


# Ruta para agregar un nuevo fabricante
@app.route("/agregar-fabricante", methods=["GET", "POST"])
def agregar_fabricante():
    form = FabricanteForm()
    service = FabricanteService()  # Instancia del servicio

    if form.validate_on_submit():
        if service.fabricante_exists(form.nombre.data):
            form.nombre.errors.append("Este fabricante ya existe.")
        else:
            service.create(
                form.nombre.data, form.pais_origen.data
            )  # Crear nuevo fabricante
            return redirect(url_for("fabricantes"))

    return render_template("agregar_fabricante.html", form=form)


# Ruta para modificar un fabricante existente
@app.route("/modificar-fabricante/<int:id>", methods=["GET", "POST"])
def modificar_fabricante(id):
    service = FabricanteService()  # Instancia del servicio
    fabricante = service.get_by_id(id)  # Obtener fabricante por ID
    form = FabricanteForm(obj=fabricante)

    if form.validate_on_submit():
        if (
            service.fabricante_exists(form.nombre.data)
            and fabricante.nombre != form.nombre.data
        ):
            form.nombre.errors.append("Este fabricante ya existe.")
        else:
            service.update(
                id, form.nombre.data, form.pais_origen.data
            )  # Actualizar fabricante
            return redirect(url_for("fabricantes"))

    form.submit.label.text = "Guardar Cambios"
    return render_template(
        "modificar_fabricante.html", form=form, fabricante=fabricante
    )


# Ruta para eliminar (ocultar) un fabricante
@app.route("/eliminar-fabricante", methods=["GET", "POST"])
def eliminar_fabricante():
    form = EmptyForm()
    service = FabricanteService()  # Instancia del servicio

    if form.validate_on_submit():
        fabricante_id = request.form.get("fabricante_id")
        if service.hide_by_id(fabricante_id):  # Ocultar fabricante
            return redirect(url_for("eliminar_fabricante"))
        else:
            form.errors["fabricante_id"] = ["Fabricante no encontrado."]

    fabricantes = service.get_active()  # Obtener fabricantes activos
    return render_template(
        "eliminar_fabricante.html", fabricantes=fabricantes, form=form
    )


# -----------------------------------------------------------------------------------------------------------------


@app.route("/restaurar", methods=["GET", "POST"])
def restaurar():
    form = EmptyForm()
    service = RestaurarService()

    if request.method == "POST":
        # Restaurar marcas
        marca_id = request.form.get("marca_id")
        if marca_id:
            service.restaurar_entidad(Marca, marca_id)

        # Restaurar categorías
        categoria_id = request.form.get("categoria_id")
        if categoria_id:
            service.restaurar_entidad(Categoria, categoria_id)

        # Restaurar modelos
        modelo_id = request.form.get("modelo_id")
        if modelo_id:
            service.restaurar_entidad(Modelo, modelo_id)

        # Restaurar proveedores
        proveedor_id = request.form.get("proveedor_id")
        if proveedor_id:
            service.restaurar_entidad(Proveedor, proveedor_id)

        # Restaurar accesorios
        accesorio_id = request.form.get("accesorio_id")
        if accesorio_id:
            service.restaurar_entidad(Accesorio, accesorio_id)

        # Restaurar fabricantes
        fabricante_id = request.form.get("fabricante_id")
        if fabricante_id:
            service.restaurar_entidad(Fabricante, fabricante_id)

        # Restaurar características
        caracteristica_id = request.form.get("caracteristica_id")
        if caracteristica_id:
            service.restaurar_entidad(Caracteristica, caracteristica_id)

        # Restaurar equipos
        equipo_id = request.form.get("equipo_id")
        if equipo_id:
            service.restaurar_entidad(Equipo, equipo_id)

        return redirect(url_for("restaurar"))

    # Recuperar todos los elementos inactivos
    marcas_inactivas = service.obtener_inactivos(Marca)
    categorias_inactivas = service.obtener_inactivos(Categoria)
    modelos_inactivos = service.obtener_inactivos(Modelo)
    proveedores_inactivos = service.obtener_inactivos(Proveedor)
    accesorios_inactivos = service.obtener_inactivos(Accesorio)
    fabricantes_inactivos = service.obtener_inactivos(Fabricante)
    caracteristicas_inactivas = service.obtener_inactivos(Caracteristica)
    equipos_inactivos = service.obtener_inactivos(Equipo)

    return render_template(
        "restaurar.html",
        marcas=marcas_inactivas,
        modelos=modelos_inactivos,
        fabricantes=fabricantes_inactivos,
        categorias=categorias_inactivas,
        proveedores=proveedores_inactivos,
        caracteristicas=caracteristicas_inactivas,
        accesorios=accesorios_inactivos,
        equipos=equipos_inactivos,
        form=form,
    )


# -----------------------------------------------------------------------------------------------------------------
@app.route("/categoria")
def categoria():
    services = CategoriaService()  # Instanciar el servicio
    categorias = services.get_active()  # Obtener solo las categorías activas
    return render_template("categoria.html", categorias=categorias)


@app.route("/agregar-categoria", methods=["GET", "POST"])
def agregar_categoria():
    form = CategoriaForm()
    services = CategoriaService()  # Instanciar el servicio
    if form.validate_on_submit():  # Validar el formulario
        if services.exists_by_name(
            form.nombre.data
        ):  # Verificar si ya existe la categoría
            form.nombre.errors.append("Esta categoría ya existe.")
        else:
            services.create(
                form.nombre.data
            )  # Crear nueva categoría usando el servicio
            return redirect(url_for("categoria"))  # Redirigir a la página de categorías
    return render_template("agregar_categoria.html", form=form)


@app.route("/modificar-categoria/<int:id>", methods=["GET", "POST"])
def modificar_categoria(id):
    services = CategoriaService()  # Instanciar el servicio
    categoria = services.get_by_id(id)  # Obtener categoría por ID
    form = CategoriaForm(obj=categoria)
    if form.validate_on_submit():
        if (
            services.exists_by_name(form.nombre.data)
            and categoria.nombre != form.nombre.data
        ):
            form.nombre.errors.append("Esta categoría ya existe.")
        else:
            services.update(
                id, form.nombre.data
            )  # Actualizar la categoría usando el servicio
            return redirect(url_for("categoria"))
    form.submit.label.text = "Guardar Cambios"
    return render_template("modificar_categoria.html", form=form, categoria=categoria)


@app.route("/eliminar-categoria", methods=["GET", "POST"])
def eliminar_categoria():
    form = CategoriaForm()  # Asegúrate de que CategoriaForm esté definido y utilizado
    services = CategoriaService()  # Instanciar el servicio
    if request.method == "POST":
        categoria_id = request.form.get("categoria_id")
        if services.hide_by_id(categoria_id):  # Ocultar categoría usando el servicio
            return redirect(url_for("eliminar_categoria"))
        else:
            form.errors["categoria_id"] = ["Categoría no encontrada."]

    categorias = services.get_active()  # Obtener solo las categorías activas
    return render_template("eliminar_categoria.html", categorias=categorias, form=form)


# -----------------------------------------------------------------------------------------------------------------
@app.route("/caracteristicas")
def caracteristicas():
    services = CaracteristicaService()  # Instanciar el servicio
    caracteristicas = services.get_active()  # Obtener solo las características activas
    return render_template("caracteristicas.html", caracteristicas=caracteristicas)


@app.route("/agregar_caracteristicas", methods=["GET", "POST"])
def agregar_caracteristicas():
    form = CaracteristicaForm()
    services = CaracteristicaService()  # Instanciar el servicio
    form.modelo_id.choices = [
        (modelo.id, modelo.nombre) for modelo in services.get_active_models()
    ]

    if form.validate_on_submit():
        services.create(
            modelo_id=form.modelo_id.data,
            peso=form.peso.data,
            resolucion_pantalla=form.resolucion_pantalla.data,
            capacidad_bateria=form.capacidad_bateria.data,
            sistema_operativo=form.sistema_operativo.data,
            precio_lista=form.precio_lista.data,
            camara=form.camara.data,
            descripcion=form.descripcion.data,
            lanzamiento=form.lanzamiento.data,
        )
        return redirect(url_for("caracteristicas"))

    return render_template("agregar_caracteristicas.html", form=form)


@app.route("/modificar-caracteristicas/<int:id>", methods=["GET", "POST"])
def modificar_caracteristicas(id):
    services = CaracteristicaService()  # Instanciar el servicio
    caracteristica = services.get_by_id(id)  # Obtener característica por ID
    form = CaracteristicaForm(obj=caracteristica)

    form.modelo_id.choices = [
        (modelo.id, modelo.nombre) for modelo in services.get_active_models()
    ]

    if form.validate_on_submit():
        services.update(
            id=id,
            modelo_id=form.modelo_id.data,
            peso=form.peso.data,
            resolucion_pantalla=form.resolucion_pantalla.data,
            capacidad_bateria=form.capacidad_bateria.data,
            sistema_operativo=form.sistema_operativo.data,
            precio_lista=form.precio_lista.data,
            camara=form.camara.data,
            descripcion=form.descripcion.data,
            lanzamiento=form.lanzamiento.data,
        )
        return redirect(url_for("caracteristicas"))

    return render_template(
        "modificar_caracteristicas.html", form=form, caracteristica=caracteristica
    )


@app.route("/eliminar-caracteristicas", methods=["GET", "POST"])
def eliminar_caracteristicas():
    form = EmptyForm()  # Usar un formulario vacío para manejar la eliminación
    services = CaracteristicaService()  # Instanciar el servicio
    if request.method == "POST":
        caracteristica_id = request.form.get("caracteristica_id")
        if services.hide_by_id(
            caracteristica_id
        ):  # Ocultar característica usando el servicio
            return redirect(url_for("eliminar_caracteristicas"))
        else:
            form.errors["caracteristica_id"] = ["Característica no encontrada."]

    caracteristicas = services.get_active()  # Obtener solo las características activas
    return render_template(
        "eliminar_caracteristicas.html", caracteristicas=caracteristicas, form=form
    )


# -----------------------------------------------------------------------------------------------------------------
@app.route("/accesorios")
def accesorios():
    services = AccesorioService()  # Instanciar el servicio
    accesorios = services.get_active()  # Obtener solo los accesorios activos
    return render_template("accesorios.html", accesorios=accesorios)


@app.route("/agregar-accesorio", methods=["GET", "POST"])
def agregar_accesorio():
    form = AccesorioForm()
    form.modelo_id.choices = [
        (modelo.id, modelo.nombre)
        for modelo in Modelo.query.filter_by(activo=True).all()
    ]

    services = AccesorioService()  # Instanciar el servicio
    if form.validate_on_submit():
        if services.exists_for_modelo(
            form.modelo_id.data
        ):  # Verificar si ya existe el accesorio
            form.modelo_id.errors.append(
                "Este accesorio ya existe para el modelo seleccionado."
            )
        else:
            services.create(
                modelo_id=form.modelo_id.data,
                cargador=form.cargador.data,
                auriculares=form.auriculares.data,
                chip=form.chip.data,
                funda=form.funda.data,
                activo=True,
            )
            return redirect(url_for("accesorios"))
    return render_template("agregar_accesorio.html", form=form)


@app.route("/modificar-accesorio/<int:id>", methods=["GET", "POST"])
def modificar_accesorio(id):
    services = AccesorioService()  # Instanciar el servicio
    accesorio = services.get_by_id(id)  # Obtener accesorio por ID
    form = AccesorioForm(obj=accesorio)
    form.modelo_id.choices = [
        (modelo.id, modelo.nombre)
        for modelo in Modelo.query.filter_by(activo=True).all()
    ]

    if form.validate_on_submit():
        if (
            services.exists_for_modelo(form.modelo_id.data)
            and accesorio.modelo_id != form.modelo_id.data
        ):
            form.modelo_id.errors.append(
                "Este accesorio ya existe para el modelo seleccionado."
            )
        else:
            services.update(
                id,
                modelo_id=form.modelo_id.data,
                cargador=form.cargador.data,
                auriculares=form.auriculares.data,
                chip=form.chip.data,
                funda=form.funda.data,
            )
            return redirect(url_for("accesorios"))
    form.submit.label.text = "Guardar Cambios"
    return render_template("modificar_accesorio.html", form=form, accesorio=accesorio)


@app.route("/eliminar-accesorios", methods=["GET", "POST"])
def eliminar_accesorios():
    form = EmptyForm()  # Usar un formulario vacío para manejar la eliminación
    services = AccesorioService()  # Instanciar el servicio
    if request.method == "POST":
        accesorio_id = request.form.get("accesorio_id")
        if services.hide_by_id(accesorio_id):  # Ocultar el accesorio usando el servicio
            return redirect(url_for("eliminar_accesorios"))
        else:
            form.errors["accesorio_id"] = ["Accesorio no encontrado."]

    accesorios = services.get_active()  # Obtener solo los accesorios activos
    return render_template("eliminar_accesorios.html", accesorios=accesorios, form=form)


# -----------------------------------------------------------------------------------------------------------------
@app.route("/equipo")
def equipos():
    services = EquipoService()  # Instanciar el servicio
    equipos = services.get_all()  # Obtener equipos activos
    return render_template("equipo.html", equipos=equipos)


@app.route("/agregar-equipos", methods=["GET", "POST"])
def agregar_equipos():
    form = EquipoForm()
    services = EquipoService()  # Instanciar el servicio
    form.categoria_id.choices = [
        (c.id, c.nombre) for c in Categoria.query.filter_by(activo=True).all()
    ]
    form.marca_id.choices = [
        (m.id, m.nombre) for m in Marca.query.filter_by(activo=True).all()
    ]
    form.modelo_id.choices = [
        (m.id, m.nombre) for m in Modelo.query.filter_by(activo=True).all()
    ]
    form.caracteristica_id.choices = [
        (c.id, f"{c.precio_lista} - {c.capacidad_bateria}")
        for c in Caracteristica.query.filter_by(activo=True).all()
    ]
    form.accesorio_id.choices = [
        (
            a.id,
            f'Cargador: {"Sí" if a.cargador else "No"}, Auriculares: {"Sí" if a.auriculares else "No"}',
        )
        for a in Accesorio.query.filter_by(activo=True).all()
    ]

    if form.validate_on_submit():
        if services.get_by_id(form.modelo_id.data):  # Verificar si el equipo ya existe
            form.modelo_id.errors.append(
                "Este equipo ya existe para el modelo seleccionado."
            )
        else:
            services.create(
                form.categoria_id.data,
                form.marca_id.data,
                form.modelo_id.data,
                form.caracteristica_id.data,
                form.accesorio_id.data,
            )
            return redirect(url_for("equipos"))
    return render_template("agregar_equipos.html", form=form)


@app.route("/modificar-equipos/<int:id>", methods=["GET", "POST"])
def modificar_equipos(id):
    services = EquipoService()  # Instanciar el servicio
    equipo = services.get_by_id(id)  # Obtener equipo por ID
    if equipo is None:
        return redirect(url_for("equipos"))  # Redirigir si no se encuentra

    form = EquipoForm(obj=equipo)

    # Cargar las opciones del formulario
    form.categoria_id.choices = [
        (c.id, c.nombre) for c in Categoria.query.filter_by(activo=True).all()
    ]
    form.marca_id.choices = [
        (m.id, m.nombre) for m in Marca.query.filter_by(activo=True).all()
    ]
    form.modelo_id.choices = [
        (m.id, m.nombre) for m in Modelo.query.filter_by(activo=True).all()
    ]
    form.caracteristica_id.choices = [
        (c.id, f"{c.precio_lista} - {c.capacidad_bateria}")
        for c in Caracteristica.query.filter_by(activo=True).all()
    ]
    form.accesorio_id.choices = [
        (
            a.id,
            f'Cargador: {"Sí" if a.cargador else "No"}, Auriculares: {"Sí" if a.auriculares else "No"}',
        )
        for a in Accesorio.query.filter_by(activo=True).all()
    ]

    if form.validate_on_submit():
        if (
            services.get_by_id(form.modelo_id.data)
            and equipo.modelo_id != form.modelo_id.data
        ):
            form.modelo_id.errors.append(
                "Este equipo ya existe para el modelo seleccionado."
            )
        else:
            equipo.categoria_id = form.categoria_id.data
            equipo.marca_id = form.marca_id.data
            equipo.modelo_id = form.modelo_id.data
            equipo.caracteristica_id = form.caracteristica_id.data
            equipo.accesorio_id = form.accesorio_id.data
            services.update(equipo)  # Actualizar el equipo usando el servicio
            return redirect(url_for("equipos"))

    form.submit.label.text = "Guardar Cambios"
    return render_template("modificar_equipos.html", form=form, equipo=equipo)


@app.route("/eliminar-equipos", methods=["GET", "POST"])
def eliminar_equipos():
    form = EmptyForm()  # Usa un formulario vacío para manejar la eliminación
    services = EquipoService()  # Instanciar el servicio
    if request.method == "POST":
        equipo_id = request.form.get("equipo_id")
        if services.hide_by_id(equipo_id):  # Ocultar el equipo usando el servicio
            return redirect(url_for("eliminar_equipos"))
        else:
            form.errors["equipo_id"] = ["Equipo no encontrado."]

    equipos = services.get_all()  # Obtener equipos activos
    return render_template("eliminar_equipos.html", equipos=equipos, form=form)


# -----------------------------------------------------------------------------------------------------------------
from services.inventario_service import InventarioService


@app.route("/inventario")
def inventario():
    services = InventarioService()  # Instanciar el servicio
    inventarios = services.get_all()  # Llama al método get_all
    return render_template("inventario.html", inventarios=inventarios)


@app.route("/agregar-inventario", methods=["GET", "POST"])
def agregar_inventario():
    services = InventarioService()  # Instanciar el servicio

    if request.method == "POST":
        nombre = request.form.get("nombre")
        proveedor_id = request.form.get("proveedor_id")
        cantidad = request.form.get("cantidad")
        fecha = request.form.get("fecha")

        # Crear un nuevo inventario
        services.create(nombre, proveedor_id, cantidad, fecha)
        return redirect(url_for("inventario"))  # Redirigir a la página de inventario

    # Cargar los modelos y proveedores para el formulario
    modelos = services.get_modelos()  # Método que obtiene los modelos activos
    proveedores = (
        services.get_proveedores()
    )  # Método que obtiene los proveedores activos
    return render_template(
        "agregar_inventario.html", modelos=modelos, proveedores=proveedores
    )


@app.route("/modificar-inventario/<int:id>", methods=["GET", "POST"])
def modificar_inventario(id):
    services = InventarioService()  # Instanciar el servicio
    inventario = services.get_by_id(id)  # Obtener inventario por ID

    if request.method == "POST":
        nuevo_nombre = request.form.get("nombre")
        nuevo_proveedor_id = request.form.get("proveedor_id")
        nueva_cantidad = request.form.get("cantidad")
        nueva_fecha = request.form.get("fecha")

        # Actualizar el inventario
        services.update(
            id, nuevo_nombre, nuevo_proveedor_id, nueva_cantidad, nueva_fecha
        )
        return redirect(url_for("inventario"))

    # Cargar proveedores para el formulario
    proveedores = (
        services.get_proveedores()
    )  # Método que obtiene los proveedores activos
    return render_template(
        "modificar_inventario.html", inventario=inventario, proveedores=proveedores
    )


@app.route("/eliminar-inventario", methods=["GET", "POST"])
def eliminar_inventario():
    services = InventarioService()  # Instanciar el servicio
    if request.method == "POST":
        inventario_id = request.form.get("inventario_id")
        services.delete_by_id(inventario_id)  # Llamar al método de eliminación
        return redirect(url_for("eliminar_inventario"))

    inventarios = services.get_all()  # Obtener todos los inventarios
    return render_template("eliminar_inventario.html", inventarios=inventarios)


# -----------------------------------------------------------------------------------------------------------------
@app.route("/cliente")
def cliente():
    cliente_service = ClienteService()  # Instanciar el servicio de cliente
    clientes = cliente_service.get_all()  # Llama al método get_all
    return render_template("cliente.html", clientes=clientes)


@app.route("/agregar-cliente", methods=["GET", "POST"])
def agregar_cliente():
    cliente_service = ClienteService()  # Instanciar el servicio de cliente
    inventario_service = InventarioService()  # Instanciar el servicio de inventario

    if request.method == "POST":
        nombre = request.form.get("nombre")
        dni = request.form.get("dni")
        inventario_id = request.form.get("inventario_id")
        fecha = request.form.get("fecha")

        # Obtener el inventario seleccionado
        inventario = inventario_service.get_by_id(inventario_id)
        if inventario and inventario.cantidad > 0:
            # Reducir la cantidad del inventario
            inventario_service.decrease_quantity(inventario_id)

            # Crear el nuevo cliente
            cliente_service.create(nombre, dni, inventario_id, fecha)
            return redirect(url_for("cliente"))
        else:
            flash("El producto seleccionado no está disponible en inventario.")

    # Cargar inventarios para el formulario
    inventarios = inventario_service.get_all()
    return render_template("agregar_cliente.html", inventarios=inventarios)


@app.route("/modificar-cliente/<int:id>", methods=["GET", "POST"])
def modificar_cliente(id):
    cliente_service = ClienteService()  # Instanciar el servicio de cliente
    inventario_service = InventarioService()  # Instanciar el servicio de inventario

    cliente = cliente_service.get_by_id(id)  # Obtener cliente por ID
    if request.method == "POST":
        nuevo_nombre = request.form.get("nombre")
        nuevo_dni = request.form.get("dni")
        nuevo_inventario_id = request.form.get("inventario_id")
        nueva_fecha = request.form.get("fecha")

        # Actualizar los datos del cliente
        cliente_service.update(
            id, nuevo_nombre, nuevo_dni, nuevo_inventario_id, nueva_fecha
        )
        return redirect(url_for("cliente"))

    # Cargar los inventarios para el formulario
    inventarios = inventario_service.get_all()
    return render_template(
        "modificar_cliente.html", cliente=cliente, inventarios=inventarios
    )


@app.route("/eliminar-cliente", methods=["GET", "POST"])
def eliminar_cliente():
    cliente_service = ClienteService()  # Instanciar el servicio de cliente
    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        cliente_service.delete_by_id(cliente_id)  # Llamar al método de eliminación
        return redirect(url_for("cliente"))

    clientes = cliente_service.get_all()  # Obtener todos los clientes
    return render_template("eliminar_cliente.html", clientes=clientes)