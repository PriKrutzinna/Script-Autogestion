# Primero crear el usuario, la mayoría de los usuarios ya existen
# Ver si el usuario ya tiene una razon social
# si tiene una razon social ver que el código de cliente sea el mismo
from os.path import join as path_join, dirname
from logger import Logger
from query_manager import QueryManager
from db_config import DB_CONFIG
from result_type import ResultType
import pandas

# get current file directory and join with /Logs
LOGGER = Logger(path_join(dirname(__file__), 'Logs'))
QUERY_MANAGER = QueryManager(path_join(dirname(__file__), 'Queries'))


def leer_tabla_excel(file_name: str, table_name: str) -> pandas.DataFrame:
    """Lee una tabla de un archivo excel y la devuelve como un DataFrame de pandas"""
    df: pandas.DataFrame = pandas.DataFrame()
    try:
        df = pandas.read_excel(file_name, sheet_name=table_name)
        return df
    except Exception as e:
        LOGGER.info(
            f"Error al leer el archivo {file_name} con la tabla {table_name}. Error: {e}")
        return df


def leer_clientes() -> pandas.DataFrame:
    return leer_tabla_excel('Datos de cliente.xlsx', 'ID_cliente')


def leer_usuarios() -> pandas.DataFrame:
    return leer_tabla_excel('Datos de usuario.xlsx', 'ID_usuario')


def procesar_usuarios():
    for usuario in leer_usuarios().to_dict(orient='records'):
        query = QUERY_MANAGER.get_query(
            'get_usuario_by_username').replace('?', usuario['ID_usuario'])
        usuarios_db_match = DB_CONFIG.execute_custom_select_query(
            query, 'autogestion_prod', ResultType.JSON_LIST)
        for u in usuarios_db_match:
            print(u)


def procesar_lista_clientes():
    for cliente in leer_clientes().to_dict(orient='records'):
        print(cliente)


procesar_usuarios()
