from data_objects.Vehicle import Vehicle
from excel_interfaces.AbstractExcelInterface import AbstractExcelInterface
from exceptions import NoExcelFileFound, NoFleetDataFound
from utility_functions import convert_dutch_string_to_boolean


class FleetInterface(AbstractExcelInterface):

    fleet: dict = {}

    print("fleet is empty now")

    def __init__(self, company: str, path_to_fleet_data: str):

        """Initialises an interface for a fleet data file.
        This interface can read from the file, but won't actually change it.
        It simulates the Excel file in memory, so "changing" a value only edits memory.

        :param path_to_fleet_data: The path to the fleet data file that the interface will interact with.
        :type path_to_fleet_data: str

        :raise NoFleetDataFound: Raised if the fleet data file can't be found or initialised.

        :return: An instance of FleetInterface.
        :rtype: FleetInterface
        """


        try:
            super().__init__(path_to_fleet_data)
        except NoExcelFileFound:
            raise NoFleetDataFound

        sheet_name = self.check_sheet_names([company, "Input wagenpark", "Input"])

        # Read fleet data
        index = 2
        reading_fleet_data = True
        while reading_fleet_data:
            
            number_plate = self.get_cell_value(sheet_name, f"A{index}")

            # If number plate is empty, stop searching
            if number_plate is None:
                reading_fleet_data = False
                continue

            vehicle_types = ['Kleine bestelwagen', 'Medium bestelwagen','Medium luxe bestelwagen','Grote bestelwagen','Kleine bakwagen (12t)','Grote bakwagen (18t)','Trekker-oplegger']

            vehicle_type = self.get_cell_value(sheet_name, f"B{index}")
            category = vehicle_types.index(vehicle_type)
            fuel_type = self.get_cell_value(sheet_name, f"C{index}")
            euronorm = self.get_cell_value (sheet_name, f"D{index}")
            year_of_purchase = self.get_cell_value(sheet_name, f"E{index}")
            is_cooled = convert_dutch_string_to_boolean(self.get_cell_value(sheet_name, f"F{index}"))
            PTO_fuel_consumption = self.get_cell_value(sheet_name, f"G{index}")
            expected_total_distance_traveled_in_km = self.get_cell_value(sheet_name, f"H{index}")
            maximum_daily_distance_in_km = self.get_cell_value(sheet_name, f"I{index}")
            amount_of_operational_days = self.get_cell_value(sheet_name, f"J{index}")
            drives_in_future_ZE_zone = convert_dutch_string_to_boolean(self.get_cell_value(sheet_name, f"K{index}"))
            technological_lifespan = self.get_cell_value(sheet_name, f"L{index}")
            loading_times = self.get_cell_value(sheet_name, f"M{index}")
            charging_time_depot = self.get_cell_value(sheet_name, f"N{index}")
            charging_time_public = self.get_cell_value(sheet_name, f"O{index}")
            electricity_type = self.get_cell_value(sheet_name, f"P{index}")

            # Add vehicle to fleet
            vehicle = Vehicle(number_plate,
                              vehicle_type,
                              int(category),
                              fuel_type,
                              int(euronorm),
                              int(year_of_purchase),
                              is_cooled,
                              int(PTO_fuel_consumption),
                              int(expected_total_distance_traveled_in_km),
                              int(maximum_daily_distance_in_km),
                              int(amount_of_operational_days),
                              drives_in_future_ZE_zone,
                              int(technological_lifespan),
                              loading_times,
                              int(charging_time_depot),
                              int(charging_time_public),
                              electricity_type)
            self.fleet[number_plate] = vehicle

            # Increment index
            index += 1
