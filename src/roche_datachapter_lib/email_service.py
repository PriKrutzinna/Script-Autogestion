"""Módulo que contiene la clase EmailDeliverySistem que se encarga de crear un registro de correo electrónico para ser enviado por Appsheet"""
from os import environ, remove
from pandas import DataFrame
from .excel_generator import ExcelGenerator
from .google_services import GoogleServices
from .appsheet_service import AppsheetService

ENV_VAR_NAMES = ["EMAIL_APPSHEET_ID", "EMAIL_APPSHEET_TOKEN",
                 "EMAIL_APPSHEET_DESTINATION_FOLDER_ID"]


class EmailService():
    """Servicio para envío de mails utilizando Appsheet"""

    def __init__(self):
        for env_var_name in ENV_VAR_NAMES:
            value = environ.get(env_var_name)
            if value is not None:
                globals()[env_var_name] = value
            else:
                raise EnvironmentError(
                    f'Environment variable "{env_var_name}" is NOT set')
        self.email_appsheet_service = AppsheetService(
            EMAIL_APPSHEET_ID, EMAIL_APPSHEET_TOKEN)  # pylint:disable=undefined-variable
        self.email_destination_folder_id = EMAIL_APPSHEET_DESTINATION_FOLDER_ID  # pylint:disable=undefined-variable
        self.email_appsheet_table_name = 'Mails'
        self.email_appsheet_folder_name = GoogleServices.get_file_name_by_file_id(
            self.email_destination_folder_id)

    def _create_excel_file_(self, p_df: DataFrame, file_name: str) -> str:
        temp_excel_file_path = ExcelGenerator.get_file_path(file_name)
        ExcelGenerator.generate_excel(p_df, temp_excel_file_path)
        file_id = GoogleServices.upload_file_to_drive(temp_excel_file_path, file_name, self.email_destination_folder_id,
                                                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        gdrive_file_name = GoogleServices.get_file_name_by_file_id(file_id)
        remove(temp_excel_file_path)
        return gdrive_file_name

    def send_email(self, to: str, subject: str, body: str, attachment_df: DataFrame, attachment_name: str, cc: str = "", bcc: str = ""):
        """Crea un registro de correo electrónico para ser enviado por Appsheet"""
        file_attachment_name = self._create_excel_file_(
            attachment_df, attachment_name)
        appsheet_post_data = [{
            "destinatario/s": to,
            "asunto": subject,
            "cuerpo": body,
            "file": f"{self.email_appsheet_folder_name}/{file_attachment_name}",
            "cc": cc,
            "bcc": bcc
        }]
        self.email_appsheet_service.add_registers_to_table(appsheet_post_data, self.email_appsheet_table_name)
