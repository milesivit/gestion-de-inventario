from db import ma
from marshmallow import validates, ValidationError

from models import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model= User
    
    id = ma.auto_field()
    username = ma.auto_field()
    password_hash = ma.auto_field()
    is_admin = ma.auto_field()
    
    @validates('username')
    def validate_username(self, value):
        user = User.query.filter_by(username=value).first()
        if user:
            raise ValidationError('Ya existe un usuario con ese username.')
        return value


class UserMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model= User
    
    username = ma.auto_field()