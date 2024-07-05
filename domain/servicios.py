"""Servicios entity module"""
from __future__ import annotations
import dataclasses
from config import DB_CONFIG, DB as db


@dataclasses.dataclass
class Servicios(db.Model):
    """Servicios class"""
    __bind_key__ = DB_CONFIG.validate_bind('autogestion_dev')
    __table_args__ = {"schema": 'public'}
    __tablename__ = 'servicios'
    servicio_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    servicio = db.Column(db.String(255))
    negocio_id = db.Column(db.Integer)
    path = db.Column(db.String(100))
    fecha_create = db.Column(db.Date)
    fecha_delete = db.Column(db.Date)
    activo = db.Column(db.Boolean)
    seccion = db.Column(db.Integer)
    image = db.Column(db.String(255))
    icono = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    rol_mapping = db.Column(db.String(255))

    def __init__(self, servicio: str, negocio_id: int, path: str,fecha_create: str,fecha_delete:str, activo: bool,seccion: int,image: str, icono: str,descripcion: str,rol_mapping: str):
        self.servicio = servicio
        self.path = path
        self.fecha_create = fecha_create
        self.fecha_delete = fecha_delete
        self.activo = activo
        self.seccion = seccion
        self.image = image
        self.icono = icono
        self.descripcion = descripcion
        self.rol_mapping = rol_mapping
        
    def __repr__(self):
        """String representation"""
        public_attributes = {
            key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        attributes = ', '.join(
            f"{key}: {value}" for key, value in public_attributes.items()
        )
        return f"{self.__class__.__name__} -> {attributes}"
