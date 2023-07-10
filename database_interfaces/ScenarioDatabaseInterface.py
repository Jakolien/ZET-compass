from database_interfaces.AbstractDatabaseInterface import AbstractDatabaseInterface

class ScenarioDatabaseInterface(AbstractDatabaseInterface):
    def __init__(self, filename='./data/data.sqlite'):
        """
        Initialises the database interface
        
        Raises:
            NoDatabaseFileFound: Raised if the database file can't be found or initialised.
        """

        super().__init__(filename)

    def read_all_scenario_data(self):
        """
        Reads all scenario data from the database.
        This includes the scenario data and the scenario names.

        Returns:
            list: A list of dictionaries containing the scenario data.
        """

        return self.read_with_join(table1="scenario_data", table2="scenario", key1="scenario")