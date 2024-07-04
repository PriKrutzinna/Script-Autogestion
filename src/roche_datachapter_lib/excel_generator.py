"""Módulo para generar archivos excel a partir de QUERYS de la base de datos"""
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side

class ExcelGenerator:
    """Clase para generar archivos excel a partir de QUERYS de la base de datos"""

    @classmethod
    def get_project_root(cls) -> str:
        """Obtiene la ruta raíz del proyecto dinámicamente."""
        return os.path.abspath(os.getcwd())

    @classmethod
    def get_file_path(cls, file_name: str) -> str:
        """Construye una ruta completa a un archivo en la raíz del proyecto."""
        if not file_name.endswith('.xlsx') and not file_name.endswith('.xls'):
            file_name += '.xlsx'
        return os.path.join(cls.get_project_root(), file_name)

    @classmethod
    def generate_excel(cls, df: pd.DataFrame, file_path: str, worksheet_name: str = 'Sheet1'):
        """Genera un archivo excel a partir de una query de la base de datos"""
        thin = Side(border_style="thin", color="000000")
        if not file_path.endswith('.xlsx') and not file_path.endswith('.xls'):
            file_path += '.xlsx'
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:  # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name=worksheet_name, index=False)
        workbook = load_workbook(file_path)
        worksheet = workbook[worksheet_name]
        for col in worksheet.columns:
            for cell in col[0:1]:  # Formatear encabezados
                cell.font = Font(name='Roboto', size=12, bold=True)
                cell.alignment = Alignment(horizontal='center')
                cell.border = Border(top=thin, left=thin,
                                     right=thin, bottom=thin)
            for cell in col[1:]:  # Formatear celdas de datos
                cell.font = Font(name='Roboto', size=10)
                cell.alignment = Alignment(horizontal='center')
                cell.border = Border(top=thin, left=thin,
                                     right=thin, bottom=thin)
        workbook.save(file_path)
