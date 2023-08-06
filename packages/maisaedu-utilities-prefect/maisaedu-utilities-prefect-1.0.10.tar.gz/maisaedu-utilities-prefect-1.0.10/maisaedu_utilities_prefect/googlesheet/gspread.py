from prefect.utilities.tasks import defaults_from_attrs
import gspread
from typing import Any, List, Union
from prefect import Task
import pathlib

class ReadGsheetRow(Task):

    def __init__(
        self,
        credentials_filename: Union[str, pathlib.Path] = None,
        sheet_key: str = None,
        worksheet_name: str = None,
        **kwargs: Any
    ):
        self.credentials_filename = credentials_filename
        self.sheet_key = sheet_key
        self.worksheet_name = worksheet_name
        super().__init__(**kwargs)

    @defaults_from_attrs("credentials_filename", "sheet_key", "worksheet_name")
    def run(
        self,
        row: int,
        credentials_filename: Union[str, pathlib.Path] = None,
        sheet_key: str = None,
        worksheet_name: str = None,
    ) -> List[Any]:
    
        client = gspread.service_account(filename=credentials_filename)
        google_sheet = client.open_by_key(sheet_key)
        worksheet = google_sheet.worksheet(worksheet_name)
        return worksheet.row_values(row)