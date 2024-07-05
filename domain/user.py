"""User entity module"""
from __future__ import annotations
import dataclasses
from domain.str_representable import StrRepresentable
from config import DB_CONFIG, DB as db


@dataclasses.dataclass
class User(db.Model, StrRepresentable):
    """User class"""
    __bind_key__ = DB_CONFIG.validate_bind('autogestion_prod')
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
        self.email = email
        self.user_id_key = user_id_key
        self.user_name = username
        self.rol_id = rol_id
        self.codigo_sap = codigo_sap
        self.usuario_admin_id = usuario_admin_id
        self.contacto_id = contacto_id
        self.activo = activo
        self.url_foto_azure = url_foto_azure
