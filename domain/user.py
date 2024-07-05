"""User entity module"""
from __future__ import annotations
import dataclasses
from data_transformer import DataTransformer
from config import DB_CONFIG, DB as db


@dataclasses.dataclass
class User(db.Model):
    """User class"""
    __bind_key__ = DB_CONFIG.validate_bind('autogestion_dev')
    __table_args__ = {"schema": 'public'}
    __tablename__ = 'usuarios'
    usuario_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255))
    user_id_key = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    rol_id = db.Column(db.Integer)
    codigo_sap = db.Column(db.String(255))
    usuario_admin_id = db.Column(db.Integer)
    contacto_id = db.Column(db.Integer)
    activo = db.Column(db.Boolean)
    url_foto_azure = db.Column(db.String(255))

    def __init__(self, email: str, user_id_key: str, username: str, rol_id: int, codigo_sap: str, usuario_admin_id: int, contacto_id: int, activo: bool, url_foto_azure: str):
        self.email = DataTransformer.nan_to_none(email)
        self.user_id_key = DataTransformer.nan_to_none(user_id_key)
        self.user_name = DataTransformer.nan_to_none(username)
        self.rol_id = DataTransformer.nan_to_none(rol_id)
        self.codigo_sap = DataTransformer.nan_to_none(codigo_sap)
        self.usuario_admin_id = DataTransformer.nan_to_none(usuario_admin_id)
        self.contacto_id = DataTransformer.nan_to_none(contacto_id)
        self.activo = DataTransformer.nan_to_none(activo)
        self.url_foto_azure = DataTransformer.nan_to_none(url_foto_azure)

    def __repr__(self):
        """String representation"""
        public_attributes = {
            key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        attributes = ', '.join(
            f"{key}: {value}" for key, value in public_attributes.items()
        )
        return f"{self.__class__.__name__} -> {attributes}"
