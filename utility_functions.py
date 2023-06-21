from base64 import b64decode, b64encode
from datetime import datetime
from tempfile import NamedTemporaryFile
from pytz import timezone


def convert_dutch_string_to_boolean(string: str):
    """
    Convert the dutch 'ja' and 'nee' strings to a boolean.

    Converts a Dutch string, if possible, into a boolean.
    Otherwise it returns the input string.

    Parameters:
    string (str): The string to convert.

    Returns:
        bool: The equivalent boolean
        str: The original string.
    """

    # Check if string is a Dutch boolean 
    # If so, return the equivalent boolean
    if string.lower() in ["ja", "nee"]:
        return string == "ja"

    # It is not, return the original string
    return string


def convert_cooled_boolean(is_cooled: bool):
    """
    Converts the is_cooled boolean into a Dutch string.

    Parameters:
        is_cooled (bool): The boolean to convert.

    Returns:
        str: The equivalent string.
    """

    # Return the equivalent Dutch string
    return "gekoeld" if is_cooled else "niet gekoeld"


def get_current_date_and_time(timezone_string: str):
    """
    Get the current date and time in the specified timezone.

    Parameters:
        timezone_string (str): The timezone to be used.

    Returns:
        str: The current date and time in the specified timezone.
    """

    # Get current date and time and return it formatted
    current_timestamp = datetime.now(tz=timezone(timezone_string))
    return current_timestamp.strftime("%Y-%m-%d_%H-%M-%S.%f")


def get_next_excel_column(current_column: str):
    """
    Get the next column name in an Excel spreadsheet.

    Parameters:
        current_column (str): The current column name.

    Returns:
        str: The next column name.
    """

    # Ensure current column name is in uppercase and setup variables
    current_column = current_column.upper()
    increment_character = True
    next_column = []

    # Loop through the characters in the current column name
    # This checks whether the column name needs to be incremented
    for char in reversed(current_column):
        if increment_character:
            if char == "Z":
                next_column.append("A")
            else:
                next_column.append(chr(ord(char)+1))
                increment_character = False
        else:
            next_column.append(char)

    # If increment character is still True, then "A" needs to be appended
    if increment_character:
        next_column.append("A")

    # Return the column string in the right order
    next_column.reverse()
    return "".join(next_column)


def base64_encode_file(file_path: str):
    """
    Encodes a file to a base 64 encoded string.

    Parameters:
        file_path (str): The path to the file to convert.

    Returns:
        str: The base 64 encoded string.
    """

    # Open the file and encode it
    data = open(file_path, 'rb').read()
    return b64encode(data).decode("UTF-8")


def base64_decode_file(encoded_string: str, file_extension: str = ".xlsx"):
    """
    Decodes a base 64 encoded string into a temporary file.

    Parameters:
        encoded_string (str): The encoded string.
        file_extension (str): The file extension of the temporary file.

    Returns:
        NamedTemporaryFile: The decoded temporary file.
    """

    # Decode the data from the string
    decoded = b64decode(encoded_string)

    # Create temporary file and write the data to it
    file = NamedTemporaryFile(suffix=file_extension, delete=False)
    file.write(decoded)
    file.seek(0)

    # Return the temporary file
    return file
