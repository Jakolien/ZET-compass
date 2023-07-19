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
        execute_query(): none
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

        Returns:
            str: The result of the query.
            list: A list of rows from the database.
        """

        # Connect to the database
        cursor = self.connect()

        # Empty the table
        result = cursor.execute(query)

        # Read the data if the query is a SELECT
        if (query.startswith("SELECT")):
            result = cursor.fetchall()

        # Disconnect from the database
        self.disconnect()

        # Return the result
        return result

    def empty_table(self, table:str):
        """
        Empties a table in the database.

        Parameters:
            table (str): The table that should be emptied.
        """

        # Log the action
        Logger.warning(f"DATABASE: Emptying {table}")

        # Empty the table
        self.execute_query(f"DELETE FROM {table}")

    def insert(self, table:str, values:dict):
        """
        Inserts a row into a table in the database.

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
        self.execute_query(f"INSERT INTO {table} ({columns}) VALUES ({data})")

    def read(self, table):
        """
        Reads all rows from a table in the database.

        Parameters:
            table (str): The table that should be read from.

        Returns:
            list: A list of rows from the table.
        """

        # Log the action
        Logger.warning(f"DATABASE: Reading from {table}")

        # Read the rows
        return self.execute_queryv(f"SELECT * FROM {table}")

    def read_with_join(self, table1:str, table2:str, key1:str="id", key2:str="id"):
        """
        Reads all the rows from two tables and combines them.

        Parameters:
            table1 (str): The first table that should be read from.
            table2 (str): The second table that should be read from.
            key1 (str): The key that should be used to join the first table, defaults to "id".
            key2 (str): The key that should be used to join the second table, defaults to "id".

        Returns:
            list: A list of rows from the tables.
        """

        # Log the action
        Logger.warning(f"DATABASE: Reading from {table1} and {table2}")

        # Read the rows
        return self.execute_query(f"SELECT * FROM {table1} JOIN {table2} ON {table1}.{key1} = {table2}.{key2}")