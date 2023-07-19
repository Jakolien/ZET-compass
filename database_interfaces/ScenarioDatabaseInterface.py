from database_interfaces.AbstractDatabaseInterface import AbstractDatabaseInterface
from data_objects.ScenarioYear import ScenarioYear
from data_objects.Scenario import Scenario
from excel_interfaces.ScenariosInterface import ScenariosInterface

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

        # Get the data from the database and convert to year objects
        data = self.read_with_join(table1="scenario_data", table2="scenario", key1="scenario")
        scenarios = [self.convert_row_into_year(x) for x in data]
        scenario_data: dict = {}

        # Loop through the scenario data and add it to the scenario data
        for sheet_name in ScenariosInterface.valid_scenario_sheet_names:
            # Prepare scenario data
            scenario_type, vehicle_type = sheet_name.split(" ")
            years = {x['scenario'].year: x['scenario'] for x in scenarios if x['sheet_name'] == sheet_name}
            scenario = Scenario(sheet_name, scenario_type, vehicle_type, years)

            # Add the scenario to the scenario data
            if scenario_type in scenario_data.keys():
                scenario_data[scenario_type][vehicle_type] = scenario
            else:
                scenario_data[scenario_type] = { vehicle_type: scenario }

        # Return the scenario data
        return scenario_data

    def convert_row_into_year(self, year_data):
        return {
            'sheet_name': year_data[72],
            'scenario': ScenarioYear(
                int(year_data[1]),
                float(year_data[2]),
                float(year_data[3]),
                int(year_data[4]),
                float(year_data[5]),
                float(year_data[6]),
                float(year_data[7]),
                float(year_data[8]),
                float(year_data[9]),
                float(year_data[10]),
                float(year_data[11]),
                float(year_data[12]),
                float(year_data[13]),
                float(year_data[14]),
                float(year_data[15]),
                float(year_data[16]),
                float(year_data[17]),
                float(year_data[18]),
                float(year_data[19]),
                float(year_data[20]),
                int(year_data[21]),
                int(year_data[22]),
                float(year_data[23]),
                float(year_data[24]),
                float(year_data[25]),
                float(year_data[26]),
                float(year_data[27]),
                float(year_data[28]),
                float(year_data[29]),
                float(year_data[30]),
                float(year_data[31]),
                float(year_data[32]),
                float(year_data[33]),
                float(year_data[34]),
                float(year_data[35]),
                float(year_data[36]),
                float(year_data[37]),
                float(year_data[38]),
                float(year_data[39]),
                float(year_data[40]),
                float(year_data[41]),
                float(year_data[42]),
                float(year_data[43]),
                float(year_data[44]),
                float(year_data[45]),
                float(year_data[46]),
                float(year_data[47]),
                float(year_data[48]),
                float(year_data[49]),
                float(year_data[50]),
                float(year_data[51]),
                float(year_data[52]),
                float(year_data[53]),
                float(year_data[54]),
                float(year_data[55]),
                float(year_data[56]),
                float(year_data[57]),
                float(year_data[58]),
                float(year_data[59]),
                float(year_data[60]),
                float(year_data[61]),
                float(year_data[62]),
                float(year_data[63]),
                float(year_data[64]),
                float(year_data[65]),
                float(year_data[66]),
                float(year_data[67]),
                float(year_data[68]),
                float(year_data[69]),
                float(year_data[70])
            )
        }