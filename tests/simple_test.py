"""Tests"""
from config import APP as app, DB as db
from domain.user import User
from domain.contact import Contact
from domain.razon_social import RazonSocial

def listar_usuarios():
    with app.app_context():
        usuarios_db = db.session.query(User).all()
        for usuario in usuarios_db:
            print(usuario)


def listar_contactos():
    with app.app_context():
        contactos_db = db.session.query(Contact).all()
        for contacto in contactos_db:
            print(contacto)


def listar_razon_social():
    with app.app_context():
        razon_social_db = db.session.query(RazonSocial).all()
        for razon_social in razon_social_db:
            print(razon_social)