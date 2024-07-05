"""Razon_social_asesores entity module"""
from __future__ import annotations
import dataclasses
from config import DB_CONFIG, DB as db


@dataclasses.dataclass
class Razon_social_asesores(db.Model):
    """Razon_social_asesores class"""
    __bind_key__ = DB_CONFIG.validate_bind('autogestion_dev')
    __table_args__ = {"schema": 'public'}
    __tablename__ = 'razon_social_asesores'
    razon_social_id = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer)


    def __init__(self, razon_social_id: int, usuario_id: int):
        self.razon_social_id = razon_social_id
        self.usuario_id = usuario_id
        
    def __repr__(self):
        """String representation"""
        public_attributes = {
            key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        attributes = ', '.join(
            f"{key}: {value}" for key, value in public_attributes.items()
        )
        return f"{self.__class__.__name__} -> {attributes}"
