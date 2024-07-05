# Primero crear el usuario, la mayoría de los usuarios ya existen, para crear un usuario se crea primero un contacto
#
from os.path import join as path_join, dirname
import logging
from datetime import datetime
import pandas
from services.query_manager import QueryManager
from config import APP as app, DB as db
from domain.result_type import ResultType
from domain.user import User
from domain.contact import Contact
from domain.razon_social import RazonSocial
from domain.rel_user_contact import UsuarioContactoRepository, UsuarioContacto

LOGGER = logging
LOGGER.basicConfig(
    filename=path_join(
        path_join(dirname(__file__), 'Logs'),
        f'process_{datetime.now().strftime(
            "%Y%m%d_%H.%M.%S")}.log',
    ),
    level=logging.DEBUG,
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)
QUERY_MANAGER = QueryManager(path_join(dirname(__file__), 'Queries'))


def leer_tabla_excel(file_name: str, table_name: str) -> pandas.DataFrame:
    """Lee una tabla de un archivo excel y la devuelve como un DataFrame de pandas"""
    df: pandas.DataFrame = pandas.DataFrame()
    try:
        with open(file_name, encoding='utf-8') as file:
            print(f"Archivo {file} encontrado")
            LOGGER.info(f"Archivo {file} encontrado")
            df = pandas.read_excel(file_name, sheet_name=table_name, dtype=str)
        return df
    except Exception as e:
        LOGGER.error(
            f"Error al leer el archivo {file_name} con la tabla {table_name}. Error: {e}")
        return df


def leer_clientes_excel() -> pandas.DataFrame:
    return leer_tabla_excel('Datos de cliente.xlsx', 'ID_cliente')


def leer_usuarios_excel() -> pandas.DataFrame:
    return leer_tabla_excel('Datos de cliente.xlsx', 'ID_usuario')


def calcular_usuarios_a_crear() -> list[dict]:
    usuarios_a_crear: list[dict] = []
    with app.app_context():
        usuarios_db = db.session.query(User).all()
        for usuario in leer_usuarios_excel().to_dict(orient='records'):
            existe = False
            for u in usuarios_db:
                if str(u.user_name).find(usuario['username']) != -1:
                    existe = True
                    break
            if not existe:
                usuarios_a_crear.append(usuario)
    return usuarios_a_crear


def crear_contacto_para_usuario() -> int:
    contacto_creado_id: int = None
    with app.app_context():
        contacto = Contact(
            apellido='',
            avatar=None,
            codigo_postal=None,
            create_fecha=datetime.now(),
            delete_fecha=None,
            direccion=None,
            dni='',
            fecha_nacimiento=None,
            nombre='Admin',
            telefono=None,
            ciudad=None
        )
        db.session.add(contacto)
        db.session.commit()
        contacto_creado_id = contacto.contacto_id
        LOGGER.info(f"CONTACTO CREADO: {contacto}")
    return contacto_creado_id


def crear_usuario(p_user_name: str, p_user_id_key: str, p_email: str, p_rol_id: int, p_contact_id: int):
    id_usuario_creado: int = None
    with app.app_context():
        usuario = User(
            email=p_email,
            user_id_key=p_user_id_key,
            username=p_user_name,
            rol_id=p_rol_id,
            codigo_sap=p_user_name,
            usuario_admin_id=None,
            contacto_id=p_contact_id,
            activo=True,
            url_foto_azure=None
        )
        db.session.add(usuario)
        db.session.commit()
        id_usuario_creado = usuario.usuario_id
        LOGGER.info(f"USUARIO CREADO: {usuario}")
    return id_usuario_creado


def actualizar_usuarios_existentes() -> list[dict]:
    results: list[dict] = []
    with app.app_context():
        usuarios_db = db.session.query(User).all()
        for usuario in leer_usuarios_excel().to_dict(orient='records'):
            usuario_existente = None
            for u in usuarios_db:
                if str(u.user_name).find(usuario['username']) != -1:
                    usuario_existente = u
            if usuario_existente and (usuario_existente.email != usuario['mail'] or usuario_existente.user_id_key != usuario['id keycloak']):
                update_obj = {
                    'usuario_id': usuario_existente.usuario_id,
                    'previous_user_id_key': usuario_existente.user_id_key,
                    'previous_email': usuario_existente.email,
                    'new_user_id_key': usuario['id keycloak'],
                    'new_email': usuario['mail']
                }
                usuario_existente.user_id_key = usuario['id keycloak']
                usuario_existente.email = usuario['mail']
                db.session.commit()
                results.append(update_obj)
                LOGGER.info(f"USUARIO ACTUALIZADO: {update_obj}")
    return results


def procesar_usuarios():
    for usuario_a_crear in calcular_usuarios_a_crear():
        new_contacto_id = crear_contacto_para_usuario()
        new_user_id = crear_usuario(
            usuario_a_crear['username'],
            usuario_a_crear['id keycloak'],
            usuario_a_crear['mail'],
            1,
            new_contacto_id
        )
    actualizar_usuarios_existentes()


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


procesar_usuarios()
