from typing import Callable
from data_objects.Vehicle import Vehicle
from excel_interfaces.AbstractExcelInterface import AbstractExcelInterface
from exceptions import NoExcelFileFound, NoFleetDataFound
from utility_functions import convert_dutch_string_to_boolean
from Logger import Logger


class FleetInterface(AbstractExcelInterface):

    # Prepare dictionaries for the fleet and errors
    fleet: dict = {}
    errors: dict = {
        "skipped_empty_rows": 0,
        "skipped_invalid_rows": {}
    }

    # Prepare a list of vehicle types, this list is private
    __vehicle_types = ['Kleine bestelwagen', 'Medium bestelwagen','Medium luxe bestelwagen','Grote bestelwagen','Kleine bakwagen (12t)','Grote bakwagen (18t)','Trekker-oplegger']

    def __init__(self, company: str, path_to_fleet_data: str):
        """
        Initialises an interface for a fleet data file.
        This interface reads fleet data from the provided file.

        Parameters:
            company (str): The company that the fleet data belongs to, this is used to find the correct sheet.
            path_to_fleet_data (str): The path to the fleet data file that the interface will interact with.

        Raises:
            NoFleetDataFound: Raised if the fleet data file can't be found or when the fleet data file doesn't contain any valid data.
        """

        # Initialise the AbstractExcelInterface
        super().__init__(path_to_fleet_data, NoFleetDataFound)

        # Get the sheet data and prepare for the loop
        # The index is set to 1 because the first row is the header
        sheet_name = self.check_sheet_names([company, "Input wagenpark", "Input"])
        reading_fleet_data = True
        empty_row_counter = 0
        index = 1

        # Loop through the fleet data for at least 50 rows
        while index < 50 or reading_fleet_data:
            # Increment the index and get the number plate
            index += 1
            number_plate = self.get_cell_value(sheet_name, f"A{index}",)

            # Check whether the row is empty, if so, save it and skip it
            if number_plate is None:
                empty_row_counter += 1
                reading_fleet_data = False
                continue

            # Check whether we encountered empty rows before, if so, add them to the error count
            elif empty_row_counter > 0:
                self.errors["skipped_empty_rows"] += empty_row_counter
                empty_row_counter = 0

            # Get the vehicle data and add it to the fleet
            try:
                self.fleet[number_plate] = self.get_vehicle(number_plate, sheet_name, index)
            
            # If the row is invalid, save it and skip it
            except Exception as e:
                self.errors["skipped_invalid_rows"][number_plate] = e

        # Check if the fleet is empty, if so, raise an error
        if len(self.fleet) == 0:
            raise NoFleetDataFound

    def get_vehicle(self, number_plate, sheet_name, index):
        """
        Get the vehicle data from the Excel sheet and create a vehicle object from it.

        Parameters:
            number_plate (str): The number plate of the vehicle.
            sheet_name (str): The name of the sheet that the vehicle data is on.
            index (int): The index of the row that the vehicle data is on.

        Raises:
            ValueError: Raised if the vehicle data is invalid.

        Returns:
            Vehicle: The vehicle object that was created from the vehicle data.
        """

        # Get all the data from the Excel sheet
        vehicle_type = self.get_cell_value(sheet_name, f"B{index}")
        category = self.__vehicle_types.index(vehicle_type)
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

        # Create the vehicle object and return it
        return Vehicle(
            self.set_vehicle_value(number_plate, "Nummerplaat"),
            self.set_vehicle_value(vehicle_type, "Vehicle Type"),
            self.set_vehicle_value(category, "Categorie", int),
            self.set_vehicle_value(fuel_type, "Brandstof type"),
            self.set_vehicle_value(euronorm, "Euronorm", int),
            self.set_vehicle_value(year_of_purchase, "Aanschafjaar", int),
            self.set_vehicle_value(is_cooled, "Gekoeld"),
            self.set_vehicle_value(PTO_fuel_consumption, "Gebruik", int),
            self.set_vehicle_value(expected_total_distance_traveled_in_km, "Verwachte afstand", int),
            self.set_vehicle_value(maximum_daily_distance_in_km, "Maximum dagelijkse afstand", int),
            self.set_vehicle_value(amount_of_operational_days, "Gebruiksdagen", int),
            self.set_vehicle_value(drives_in_future_ZE_zone, "Ritten in ZE zone"),
            self.set_vehicle_value(technological_lifespan, "Levensverwachting", int),
            self.set_vehicle_value(loading_times, "Laadtijd"),
            self.set_vehicle_value(charging_time_depot, "Oplaadtijd depot", int),
            self.set_vehicle_value(charging_time_public, "Oplaadtijd publiekelijk", int),
            self.set_vehicle_value(electricity_type, "Elektricteitstype")
        )

    def set_vehicle_value(self, value: str, value_name: str, conversion: Callable[[str], any]=lambda x: x):
        """
        Perform a check on the vehicle data and convert it to the correct type if necessary.

        Parameters:
            value (str): The value that needs to be checked and converted.
            value_name (str): The name of the value that needs to be checked and converted, used for error messages.
            conversion (Callable[[str], any]): The function that needs to be used to convert the value.

        Raises:
            ValueError: Raised if the value is invalid.

        Returns:
            any: The converted value.
        """
        # Check and convert the value
        try: return conversion(value)

        # If the value is invalid, raise an error
        except Exception as e:
            raise ValueError(f"{value_name} is niet geschikt voor gebruik, het voertuig wordt overgeslagen...")
