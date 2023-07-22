from typing import Union
from exceptions import NoExcelFileFound, PANTEIAModelError
from pycel import ExcelCompiler


class AbstractExcelInterface:

    file_name: str = None
    excel_model: ExcelCompiler = None

    def __init__(self, path_to_excel, error: Exception=NoExcelFileFound):

        """Initialises an interface for an Excel file.
        This interface can read from the file, but won't actually change it.
        It simulates the Excel file in memory, so "changing" a value only edits memory.
        NOTE: Don't initialise this class directly. Please create a custom class.

        :param path_to_excel: The path to the Excel file that the interface will interact with.
        :type path_to_excel: str

        :raise NoExcelFileFound: Raised if the Excel file can't be found or initialised.

        :return: An instance of AbstractExcelInterface.
        :rtype: AbstractExcelInterface
        """

        try:
            self.excel_model = ExcelCompiler(filename=path_to_excel)
        except:
            raise error

    def check_sheet_names(self, names: list):
        """
        
        """

        for name in names:
            try:
                self.excel_model.evaluate(f"{name}!A1")
                return name
            except: 
                continue

        return None

    def get_cell_value(self, sheet_name: str, cell_address: str, backup_sheet_name: str=None):

        """Gets the value of the specified cell.
        :param sheet_name: The name of the Excel Worksheet.
        :type: str
        :param cell_address: The address of the cell. Consists of a column and row number. Example: A14.
        :type: str

        :return: The value of the cell.
        :rtype: str
        """

        # Return the cell address
        return self.excel_model.evaluate(f"{sheet_name}!{cell_address}")

    def set_cell_value(self, sheet_name: str, cell_address: str, value: any):

        """Sets the value of the specified cell in memory.
        NOTE: This doesn't actually change the value in the file.

        :param sheet_name: The address of the cell. Consists of a column and row number. Example: A14.
        :type: str
        :param cell_address: The address of the cell. Consists of a column and row number. Example: A14.
        :type: str
        :param value: The value that the cell should be set to.
        :type: any

        :return: Nothing
        :rtype: None
        """

        try:
            self.get_cell_value(sheet_name, cell_address)
            self.excel_model.set_value(f"{sheet_name}!{cell_address}", value)
        except:
            raise PANTEIAModelError
