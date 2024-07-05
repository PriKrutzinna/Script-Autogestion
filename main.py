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
        for usuario in leer_usuarios().to_dict(orient='records'):
            existe = False
            usuario_existente=None
            for u in usuarios_db:
                #check if string contains substring
                if str(u.user_name).find(usuario['username'])!=-1 :
                    existe = True
                    usuario_existente=u
            if existe:
                print(f"Usuario {usuario['username']} existe en la base de datos. Usuario existente: {usuario_existente.usuario_id}")
            else:
                print(f"Usuario {usuario['username']} NO existe en la base de datos")
            # if len(usuarios_db_match) == 0:
            #    query = QUERY_MANAGER.get_query(
            #        'insert_usuario').replace('?', usuario['ID_usuario'])
            #    DB_CONFIG.execute_custom_select_query(
            #        query, 'autogestion_prod', ResultType.JSON_LIST)



crear_usuarios_inexsistentes()
