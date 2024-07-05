"""All Database configurations and methods"""
from typing import List, Dict, Any
from os import environ
import pandas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from result_type import ResultType

ENV_VAR_NAMES = ["AUTOGESTION_PROD_DB_SERVER", "AUTOGESTION_PROD_DB_PORT", "AUTOGESTION_PROD_DB_DATABASE",
                 "AUTOGESTION_PROD_DB_USER", "AUTOGESTION_PROD_DB_PWD",
                 "AUTOGESTION_DEV_DB_SERVER", "AUTOGESTION_DEV_DB_PORT", "AUTOGESTION_DEV_DB_DATABASE",
                 "AUTOGESTION_DEV_DB_USER", "AUTOGESTION_DEV_DB_PWD",]

for env_var_name in ENV_VAR_NAMES:
    value = environ.get(env_var_name)
    if value is not None:
        globals()[env_var_name] = value
    else:
        raise EnvironmentError(
            f'Environment variable "{env_var_name}" is NOT set')


class DbConfig():
    """DB config params"""
    SQLALCHEMY_BINDS = {
        'autogestion_prod': f'postgresql+psycopg2://{AUTOGESTION_PROD_DB_USER}:{AUTOGESTION_PROD_DB_PWD}@{AUTOGESTION_PROD_DB_SERVER}:{AUTOGESTION_PROD_DB_PORT}/{AUTOGESTION_PROD_DB_DATABASE}',  # pylint:disable=undefined-variable
        'autogestion_dev': f'postgresql+psycopg2://{AUTOGESTION_DEV_DB_USER}:{AUTOGESTION_DEV_DB_PWD}@{AUTOGESTION_DEV_DB_SERVER}:{AUTOGESTION_DEV_DB_PORT}/{AUTOGESTION_DEV_DB_DATABASE}',  # pylint:disable=undefined-variable
    }

    @classmethod
    def __get_bind__(cls, bind: str = ''):
        return cls.SQLALCHEMY_BINDS[cls.validate_bind(bind)]

    @classmethod
    def __check_select_query__(cls, query: str = ''):
        if not query.lower().strip().startswith("select"):
            raise ValueError(f'NOT SELECT query: "{query[:100].strip().replace(
                '\n', ' ').replace('\t', ' ').replace('  ', ' ')}..."')

    @classmethod
    def validate_bind(cls, bind: str = ''):
        """Bind validation"""
        if bind in cls.SQLALCHEMY_BINDS:
            return bind
        available_binds = ', '.join(
            f"{key}" for key in cls.SQLALCHEMY_BINDS)
        raise ValueError(
            f'Bind Key "{bind}" NOT valid. Available binds are: {available_binds}')

    @classmethod
    def test_bind_connection(cls, bind: str = ''):
        """Bind testing. Return True if connection success, otherwise return False"""
        try:
            engine = create_engine(cls.__get_bind__(bind), echo=True)
            with engine.connect():
                return True
        except OperationalError:
            return False
        return False

    @classmethod
    def execute_custom_select_query(cls, query: str, p_bind: str, result_set_as: ResultType = ResultType.PANDAS_DATA_FRAME) -> pandas.DataFrame | List[Dict[str, Any]]:
        """Execute SQL SELECT query on specific bind and return result set as a pandas DataFrame"""
        cls.__check_select_query__(query)
        df = pandas.DataFrame()
        engine = create_engine(cls.__get_bind__(p_bind))
        with engine.connect() as connection:
            result = connection.execute(text(query))
            all_rows = result.fetchall()
            if len(all_rows) > 0:
                df = pandas.DataFrame.from_records(
                    all_rows, columns=result.keys())
        if result_set_as == ResultType.JSON_LIST:
            df = df.to_dict(orient='records')
        return df

    @classmethod
    def execute_stored_procedure(cls, sp_name: str, sp_params: dict = None, p_bind: str = 'sqlserver_master'):
        """Execute SQL query on specific bind and return result set as a dictionary"""
        engine = create_engine(cls.__get_bind__(p_bind))
        with engine.connect() as connection:
            sql_string = f"EXEC {sp_name} "
            params = []
            if isinstance(sp_params, dict):
                for clave, valor in sp_params.items():
                    if not clave.startswith('@'):
                        clave = f'@{clave}'
                    if isinstance(valor, str):
                        params.append(f"{clave}=N'{valor}'")
                    elif isinstance(valor, bool):
                        params.append(f"{clave}={1 if valor else 0}")
                    elif isinstance(valor, (int, float)):
                        params.append(f"{clave}={repr(valor)}")
                    else:
                        print(type(valor))
                        input(valor)
                        raise ValueError(
                            "sp_params only accept dict of int, float, bool or str")
                sql_string += ', '.join(params)
            connection.execute(text(sql_string))
            connection.commit()

    @classmethod
    def truncate_table(cls, p_bind: str, schema: str, table: str):
        """Truncate specific table from specific bind"""
        engine = create_engine(cls.__get_bind__(p_bind))
        with engine.connect() as connection:
            sql_string = f"TRUNCATE TABLE [{str(schema)}].[{str(table)}]"
            connection.execute(text(sql_string))
            connection.commit()
            return True
        return False


DB_CONFIG = DbConfig()

APP = Flask(__name__)
APP.config.from_object(DbConfig())
DB = SQLAlchemy(APP)
