from base64 import b64decode, b64encode
from tempfile import NamedTemporaryFile


def convert_dutch_string_to_boolean(string: str):

    """Converts a Dutch string, if possible, into a boolean.
    Otherwise it returns the input string.

    :param string: The string to convert.
    :type string: str

    :return: The equivalent boolean or the original string.
    :rtype: bool or str
    """

    if string.lower() == "ja":
        return True

    if string.lower() == "nee":
        return False

    # Return original string, if conversion isn't possible
    return string


def convert_cooled_boolean(is_cooled: bool):

    """Converts the is_cooled boolean into a Dutch string.

    :param is_cooled: The boolean to convert.
    :type is_cooled: bool

    :return: The equivalent string.
    :rtype: str
    """

    if is_cooled:
        return "gekoeld"
    else:
        return "niet gekoeld"


def get_next_excel_column(current_column: str):

    """Get the next column name in an Excel spreadsheet.

    :param current_column: The current column name.
    :type: str

    :return: The next column name.
    :rtype: str
    """

    # Ensure current column name is in uppercase
    current_column = current_column.upper()

    increment_character = True
    next_column = []
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

    """Encodes a file to a base 64 encoded string.

    :param file_path: The path to the file to convert.
    :type file_path: str

    :return: The encoded string.
    :rtype: str
    """

    data = open(file_path, 'rb').read()
    encoded = b64encode(data).decode("UTF-8")

    return encoded


def base64_decode_file(encoded_string: str, file_extension: str = ".xlsx"):

    """Decodes a base 64 encoded string into a temporary file.

    :param encoded_string: The encoded string.
    :type encoded_string: str
    :param file_extension: The file extension of the temporary file.
    :type file_extension: str

    :return: The decoded temporary file.
    :rtype: NamedTemporaryFile
    """

    # Decode string
    decoded = b64decode(encoded_string)

    # Create temporary file
    file = NamedTemporaryFile(suffix=file_extension)
    file.write(decoded)
    file.seek(0)

    return file
