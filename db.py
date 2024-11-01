from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow(db)

# esto me generaba error circular, fue la unica solucion que encontre ya que
# no me ayudo ni el chat
# :)
