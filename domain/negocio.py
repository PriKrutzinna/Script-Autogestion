"""Negocio entity module"""
from __future__ import annotations
import dataclasses
from config import DB_CONFIG, DB as db


@dataclasses.dataclass
class Negocio(db.Model):
    """Negocio class"""
    __bind_key__ = DB_CONFIG.validate_bind('autogestion_dev')
    __table_args__ = {"schema": 'public'}
    __tablename__ = 'negocio'
    negocio_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    negocio = db.Column(db.String(255))


    def __init__(self, negocio: str):
        self.negocio = negocio
        
    def __repr__(self):
        """String representation"""
        public_attributes = {
            key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        attributes = ', '.join(
            f"{key}: {value}" for key, value in public_attributes.items()
        )
        return f"{self.__class__.__name__} -> {attributes}"
