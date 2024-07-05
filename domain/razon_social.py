"""Razon social entity module"""
from __future__ import annotations
import dataclasses
from config import DB_CONFIG, DB as db


@dataclasses.dataclass
class RazonSocial(db.Model):
    """Razon social class"""
    __bind_key__ = DB_CONFIG.validate_bind('autogestion_prod')
    __table_args__ = {"schema": 'public'}
    __tablename__ = 'razon_social'
    razon_social_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    activo = db.Column(db.Boolean)
    codigo_cliente = db.Column(db.String(255))
    cuit_destino = db.Column(db.String(255))
    cuit_origen = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    estado = db.Column(db.Boolean)
    fecha_validacion = db.Column(db.DateTime)
    numero_factura = db.Column(db.String(255))
    razon_social= db.Column(db.String(255))
    telefono= db.Column(db.String(255))
    usuario_id= db.Column(db.Integer)
    grupo_id= db.Column(db.Integer)
    user_id_invgate= db.Column(db.String(10))
    cta_cte_id= db.Column(db.Integer)

    def __init__(self, activo: bool, codigo_cliente: str, cuit_destino: str, cuit_origen: str, direccion: str, estado: bool, fecha_validacion: str, numero_factura: str, razon_social: str, telefono: str, usuario_id: int, grupo_id: int, user_id_invgate: str, cta_cte_id: int):
        self.activo = activo
        self.codigo_cliente = codigo_cliente
        self.cuit_destino = cuit_destino
        self.cuit_origen = cuit_origen
        self.direccion = direccion
        self.estado = estado
        self.fecha_validacion = fecha_validacion
        self.numero_factura = numero_factura
        self.razon_social = razon_social
        self.telefono = telefono
        self.usuario_id = usuario_id
        self.grupo_id = grupo_id
        self.user_id_invgate = user_id_invgate
        self.cta_cte_id = cta_cte_id
        
    def __repr__(self):
        """String representation"""
        public_attributes = {
            key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        attributes = ', '.join(
            f"{key}: {value}" for key, value in public_attributes.items()
        )
        return f"{self.__class__.__name__} -> {attributes}"
