from .auth_views import auth_bp
from .modelos_views import modelo_bp
from .caracteristica_views import caracteristica_bp
from .equipo_views import equipo_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(modelo_bp)
    app.register_blueprint(caracteristica_bp)
    app.register_blueprint(equipo_bp)