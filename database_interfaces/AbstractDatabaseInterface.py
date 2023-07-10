from exceptions import NoDatabaseFileFound
from Logger import Logger
import os, sqlite3

class AbstractDatabaseInterface:
    """
    An interface for a SQLite database.
    Please create a custom class that inherits from this class.

    Implements:
        connect(): sqlite3.Cursor
        empty_table(): none
    """

    filename: str = None
    database_connection: sqlite3.Connection = None

    def __init__(self, filename='./data/data.sqlite'):
        """
        Initialises an interface for a SQLite database.
        Sets the filename and checks if the file exists.
        
        Raises:
            NoDatabaseFileFound: Raised if the database file can't be found or initialised.
        """

        # Set the filename
        self.filename = filename

        # Check if the file exists or error out
        if not os.path.isfile(self.filename):
            raise NoDatabaseFileFound

    def connect(self):
        """
        Connects to the database and returns a cursor.
        A connection is only made if there isn't already a connection.

        Returns:
            sqlite3.Cursor: A cursor that can be used to interact with the database.
        """

        # Check if there is already a connection
        if (self.database_connection is None):
            # Connect to the database and return a cursor
            self.database_connection = sqlite3.connect(self.filename)
            return self.database_connection.cursor()

    def disconnect(self):
        """
        Disconnects from the database.
        Removes the connection values and commits the changes.

        Parameters:
            cursor (sqlite3.Cursor): The cursor that was used to interact with the database.
        """

        # Commit the changes and close the connection
        self.database_connection.commit()
        self.database_connection.close()
        self.database_connection = None

    def execute_query(self, query:str):
        """
        Executes a query on the database.
        Creates a connection, executes the query and disconnects.

        Parameters:
            query (str): The query that should be executed.
        """

        # Connect to the database
        cursor = self.connect()

        # Empty the table
        cursor.execute(query)

        # Disconnect from the database
        self.disconnect()

    def empty_table(self, table:str):
        """
        Empties a table in the database.
        Creates a connection, empties the table and disconnects.

        Parameters:
            table (str): The table that should be emptied.
        """

        # Log the action
        Logger.warning(f"DATABASE: Emptying {table}")

        # Empty the table
        self.execute(f"DELETE FROM {table}")

    def insert(self, table:str, values:dict):
        """
        Inserts a row into a table in the database.
        Creates a connection, inserts the row and disconnects.

        Parameters:
            table (str): The table that the row should be inserted into.
            values (dict): The data that should be inserted into the row. Formatted as key-value pairs [column: value].
        """

        # Log the action
        Logger.warning(f"DATABASE: Inserting row into {table}")

        # Create the columns and values strings
        columns = ", ".join(values.keys())
        data = ", ".join([f"'{value}'" for value in values.values()])

        # Insert the row
        self.execute(f"INSERT INTO {table} ({columns}) VALUES ({data})")

    def read(self, table):
        """
        Reads all rows from a table in the database.
        Creates a connection, reads the rows and disconnects.

        Parameters:
            table (str): The table that should be read from.

        Returns:
            list: A list of rows from the table.
        """

        # Log the action
        Logger.warning(f"DATABASE: Reading from {table}")

        # Read the rows
        return self.execute(f"SELECT * FROM {table}")