import sys

from datetime import datetime
from logging import basicConfig, error, info, warning
from os import makedirs
from os.path import isdir
from pytz import timezone, utc
from traceback import format_exception


class Logger:

    def __init__(self, tz: str = utc, level: str = "WARNING"):

        """Initialises a Logger.

        :param tz: The timezone to be used.
        :param level: The minimum level of messages to be logged. See the logging documentation for more information.
        """

        # Check if logs directory exists
        if not isdir("logs"):
            makedirs("logs")

        # Format datetime string
        current_timestamp = datetime.now(tz=timezone(tz))
        datetime_string = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S.%f")

        basicConfig(filename=f"logs/{datetime_string}.log",
                    filemode="w",
                    format="[%(asctime)s] %(levelname)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=level.upper())

        sys.excepthook = self.exception

    def log(self, message: str):

        """Log an informative message.

        :param message: The message to log.

        :return: Nothing
        :rtype: None
        """

        info(message)

    def warning(self, message: str):

        """Log an warning message.

        :param message: The warning to log.

        :return: Nothing
        :rtype: None
        """

        warning(message)

    def error(self, message: str):

        """Log an error message.

        :param message: The error to log.

        :return: Nothing
        :rtype: None
        """

        error(message)

    def exception(self, exctype, value, tb):

        """Log a formatted Exception.

        :param exctype: The Exception type.
        :param value: The Exception message.
        :param tb: The traceback message.

        :return: Nothing
        :rtype: None
        """

        lines = format_exception(exctype, value, tb)
        self.error(lines)
