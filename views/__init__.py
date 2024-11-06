from .auth_views import auth_bp
from .equipo_views import equipo_bp



def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipo_bp)
 