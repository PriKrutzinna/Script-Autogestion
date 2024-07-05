"""Contact entity module"""
from __future__ import annotations
import dataclasses
from config import DB_CONFIG, DB as db


@dataclasses.dataclass
class Contact(db.Model):
    """Contact class"""
    __bind_key__ = DB_CONFIG.validate_bind('autogestion_prod')
    __table_args__ = {"schema": 'public'}
    __tablename__ = 'contactos'
    contacto_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    apellido = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    codigo_postal = db.Column(db.String(255))
    create_fecha = db.Column(db.DateTime)
    delete_fecha = db.Column(db.DateTime)
    direccion = db.Column(db.String(255))
    dni = db.Column(db.String(255))
    fecha_nacimiento = db.Column(db.DateTime)
    nombre = db.Column(db.String(255))
    telefono= db.Column(db.String(255))
    ciudad= db.Column(db.String(255))

    def __init__(self, apellido: str, avatar: str, codigo_postal: str, create_fecha: str, delete_fecha: str, direccion: str, dni: str, fecha_nacimiento: str, nombre: str, telefono: str, ciudad: str):
        self.apellido = apellido
        self.avatar = avatar
        self.codigo_postal = codigo_postal
        self.create_fecha = create_fecha
        self.delete_fecha = delete_fecha
        self.direccion = direccion
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.nombre = nombre
        self.telefono = telefono
        self.ciudad = ciudad
        
    def __repr__(self):
        """String representation"""
        public_attributes = {
            key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        attributes = ', '.join(
            f"{key}: {value}" for key, value in public_attributes.items()
        )
        return f"{self.__class__.__name__} -> {attributes}"
