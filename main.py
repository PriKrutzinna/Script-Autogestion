# Primero crear el usuario, la mayoría de los usuarios ya existen, para crear un usuario se crea primero un contacto
#
from os.path import join as path_join, dirname
import logging
from datetime import datetime
import pandas
from services.query_manager import QueryManager
from config import APP as app, DB as db
from data_transformer import DataTransformer
from domain.user import User
from domain.contact import Contact
from domain.razon_social import RazonSocial

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
            df = pandas.read_excel(file_name, sheet_name=table_name, dtype=str)
            LOGGER.info(
                f"Archivo '{file_name}' tabla '{table_name}' leído correctamente.")
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
        LOGGER.info(f"{len(usuarios_db)} Usuarios a procesar")
        usuarios_procesados = 0
        for usuario in leer_usuarios_excel().to_dict(orient='records'):
            usuario_existente = None
            for u in usuarios_db:
                if str(u.user_name).find(usuario['username']) != -1:
                    usuario_existente = u
                    break
            new_user_id_key: str = DataTransformer(usuario['id keycloak'])
            new_email: str = DataTransformer(usuario['mail'])
            if usuario_existente and (usuario_existente.email != new_email or usuario_existente.user_id_key != new_user_id_key):
                update_obj = {
                    'usuario_id': usuario_existente.usuario_id,
                    'previous_user_id_key': usuario_existente.user_id_key,
                    'previous_email': usuario_existente.email,
                    'new_user_id_key': new_user_id_key,
                    'new_email': new_email
                }
                usuario_existente.user_id_key = new_user_id_key
                usuario_existente.email = new_email
                results.append(update_obj)
                LOGGER.info(f"USUARIO A ACTUALIZAR: {update_obj}")
            usuarios_procesados += 1
            print(
                f"Usuarios procesados en actualizacion: {usuarios_procesados}")
        LOGGER.info(
            f"INICIANDO COMMIT DE ACTUALIZACION ({len(results)} usuarios)")
        db.session.commit()
        LOGGER.info(
            f"USUARIOS ACTUALIZADOS CORRECTAMENTE ({len(results)} usuarios)")
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
    LOGGER.info("INICIANDO ACTUALIZACION DE USUARIOS")
    actualizar_usuarios_existentes()


procesar_usuarios()
LOGGER.info("PROCESO FINALIZADO")
