# Primero crear el usuario, la mayoría de los usuarios ya existen, para crear un usuario se crea primero un contacto
#
from os.path import join as path_join, dirname
import logging
from datetime import datetime
import pandas
from query_manager import QueryManager
from config import APP as app, DB as db
from result_type import ResultType
from domain.user import User
from domain.contact import Contact

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
        # leer primero el archivo para verificar si existe, luego pasarle el archivo leído a la función read_excel
        with open(file_name, encoding='utf-8') as file:
            print(f"Archivo {file} encontrado")
            LOGGER.info(f"Archivo {file} encontrado")
            #crear un dataframe con los resultados pero todos con tipo de dato string, no dejar que pandas tipe los datos
            df = pandas.read_excel(file_name, sheet_name=table_name, dtype=str)
        return df
    except Exception as e:
        LOGGER.error(
            f"Error al leer el archivo {file_name} con la tabla {table_name}. Error: {e}")
        return df


def leer_clientes() -> pandas.DataFrame:
    return leer_tabla_excel('Datos de cliente.xlsx', 'ID_cliente')


def leer_usuarios() -> pandas.DataFrame:
    return leer_tabla_excel('Datos de cliente.xlsx', 'ID_usuario')


def crear_usuarios_inexsistentes():
    with app.app_context():
        usuarios_db=db.session.query(User).all()
        usuarios_existentes: list[User] = []
        usuarios_a_crear: list[dict] = []
        for usuario in leer_usuarios().to_dict(orient='records'):
            existe = False
            usuario_existente=None
            for u in usuarios_db:
                #check if string contains substring
                if str(u.user_name).find(usuario['username'])!=-1 :
                    existe = True
                    usuario_existente=u
            if existe:
                usuarios_existentes.append(usuario_existente)
            else:
                usuarios_a_crear.append(usuario)
        print(f"Usuarios existentes: {len(usuarios_existentes)}")
        for usuario in usuarios_existentes:
            print(usuario)
        print(f"Usuarios a crear: {len(usuarios_a_crear)}")
        for usuario in usuarios_a_crear:
            print(usuario)
            
def crear_contactos_inexistentes():
    withn app.app_context():
        contactos_db=db.session.query(Contact).all()
        for contacto in contactos_db:
            print(contacto)



crear_contactos_inexistentes()
