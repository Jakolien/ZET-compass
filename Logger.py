import sys
import logging

from os import makedirs
from os.path import isdir
from traceback import format_exception
from utility_functions import get_current_date_and_time


class Logger:
    """
    A class used to log messages to a file.
    Also logs Python exceptions.
    """

    def __init__(self, timezone_string: str = "utc", level: str = "WARNING"):
        """
        Initialises a Logger.

        Initialises a Logger and sets the exception hook.
        The Logger will log messages to a file in the logs directory.
        The filename is the current date and time in the specified timezone.

        Parameters:
            [optional] timezone_string (str): The timezone to be used.
            Defaults to "utc".

            [optional] level: The minimum level of messages to be logged. 
            See the logging documentation for more information.
            Defaults to "WARNING".
        """

        # Initialize the logs directory and set the exception hook
        # The exception hook is used to log Python exceptions
        self.initialize_logs_directory()
        sys.excepthook = self.exception

        # Get the current date and time in the specified timezone
        now = get_current_date_and_time(timezone_string)
        
        # Initialize the logger
        logging.basicConfig(
            filename=f"logs/{now}.log",
            filemode="w",
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=level.upper()
        )        

    def initialize_logs_directory(self):
        """
        Initialize the logs directory

        Check whether the logs directory exist.
        If it doesn't exists, it's created.
        """

        # Check if logs directory exists, create it if not
        if not isdir("logs"):
            makedirs("logs")

    def log(self, message: str):
        """
        Log an informative message.

        Parameters:
            message (str): The message to log.
        """

        # Log the message
        logging.info(message)

    def warning(self, message: str):
        """
        Log an warning message.

        Parameters:
            message (str): The warning to log.
        """

        # Log the warning
        logging.warning(message)

    def error(self, message: str):
        """
        Log an error message.

        Parameters:
            message (str): The error to log.
        """

        # Log the error
        logging.error(message)

    def exception(self, exception_type, message, traceback):
        """
        Log a formatted Exception.

        This function is used as the exception hook.
        It logs the Exception to the log file.

        Parameters:
            exception_type (any): The Exception type.
            message (any): The Exception message.
            traceback (any): The traceback message.
        """

        # Format the Exception
        lines = format_exception(exception_type, message, traceback)

        # Log the Exception as an error
        self.error(lines)
