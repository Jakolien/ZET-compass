from typing import Callable
from data_objects.Vehicle import Vehicle
from excel_interfaces.AbstractExcelInterface import AbstractExcelInterface
from exceptions import NoFleetDataFound
from utility_functions import convert_dutch_string_to_boolean as string_to_boolean


class FleetInterface(AbstractExcelInterface):
    """
    The fleet interface helps to read fleet data from an Excel file.
    The attributes of the class are accessible after initialisation.
    They can be used to get all the data.

    Attributes:
        fleet (dict): A dictionary containing all the vehicles in the fleet.
        errors (dict): A dictionary containing all the errors that occurred during the initialisation.
    """

    # Prepare a list of vehicle types and one for defaulted values, these lists are private
    __types = ['Kleine bestelwagen', 'Medium bestelwagen','Medium luxe bestelwagen','Grote bestelwagen','Kleine bakwagen (12t)','Grote bakwagen (18t)','Trekker-oplegger']


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

        # Prepare dictionaries for the fleet and errors
        self.fleet: dict = {}
        self.defaulted_values = []
        self.errors: dict = {
            "skipped_empty_rows": 0,
            "skipped_invalid_rows": {},
            "defaulted_values": {}
        }

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

            # Check whether the row is the example, if so, skip it
            if number_plate.lower() == "voorbeeld" or number_plate == "G258TD":
                continue

            # Check whether we encountered empty rows before, if so, add them to the error count
            elif empty_row_counter > 0:
                self.errors["skipped_empty_rows"] += empty_row_counter
                empty_row_counter = 0
                reading_fleet_data = True

            # Get the vehicle data and add it to the fleet, process the defaulted values
            try:
                self.fleet[number_plate] = self.get_vehicle(number_plate, sheet_name, index)
                self.process_defaulted_values(number_plate)
            
            # Check if the vehicle data is invalid
            except Exception as e:
                # Save the error and clear the defaulted values for this vehicle
                self.errors["skipped_invalid_rows"][number_plate] = e
                self.defaulted_values = []

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

        # Get the vehicle data and remove any leading/trailing whitespace
        vehicle_data = self.get_cell_value(sheet_name, f"B{index}:P{index}")
        vehicle_data = [str(cell).strip() for cell in vehicle_data]

        # Create the vehicle object and return it
        return Vehicle(
            self.set_vehicle_value(number_plate, "Nummerplaat"),
            self.set_vehicle_value(vehicle_data[0], "Vehicle Type"),
            self.set_vehicle_value(vehicle_data[0], "Categorie", self.__types.index),
            self.set_vehicle_value(vehicle_data[1], "Brandstof type", default="Diesel"),
            self.set_vehicle_value(vehicle_data[2], "Euronorm", int, 6),
            self.set_vehicle_value(vehicle_data[3], "Aanschafjaar", int),
            self.set_vehicle_value(vehicle_data[4], "Gekoeld", string_to_boolean, False),
            self.set_vehicle_value(vehicle_data[5], "Gebruik", int, 0),
            self.set_vehicle_value(vehicle_data[6], "Verwachte afstand", int),
            self.set_vehicle_value(vehicle_data[7], "Maximum dagelijkse afstand", int, 200),
            self.set_vehicle_value(vehicle_data[8], "Gebruiksdagen", int, 220),
            self.set_vehicle_value(vehicle_data[9], "Ritten in ZE zone", string_to_boolean, False),
            self.set_vehicle_value(vehicle_data[10], "Levensverwachting", int, 7),
            self.set_vehicle_value(vehicle_data[11], "Laadtijd", default="Combinatie"),
            self.set_vehicle_value(vehicle_data[12], "Oplaadtijd depot", int, 8),
            self.set_vehicle_value(vehicle_data[13], "Oplaadtijd publiekelijk", int, 3),
            self.set_vehicle_value(vehicle_data[14], "Elektricteitstype", default="Groen")
        )

    def set_vehicle_value(self, value: str, value_name: str, conversion: Callable[[str], any]=lambda x: x, default=None):
        """
        Perform a check on the vehicle data and convert it to the correct type if necessary.

        Parameters:
            value (str): The value that needs to be checked and converted.
            value_name (str): The name of the value that needs to be checked and converted, used for error messages.
            conversion (Callable[[str], any]): The function that needs to be used to convert the value.
            default (any): The default value that needs to be returned if the value is invalid.

        Raises:
            ValueError: Raised if the value is invalid.

        Returns:
            any: The converted value.
        """
        # Check and convert the value
        try: return conversion(value)

        # If the value is invalid, return the default value if it is set
        except Exception as e:
            # Check if a default value is set, if so, return it
            if default is not None:
                self.defaulted_values.append(f"{value_name} naar {default}")
                return default

            # If no default value is set, raise an error
            raise ValueError(f"{value_name} is verplicht en niet geschikt voor gebruik, het voertuig wordt overgeslagen...")

    def process_defaulted_values(self, number_plate: str):
        """
        Process the defaulted values and add them to the errors if necessary.
        Empty the defaulted values list afterwards.

        Parameters:
            number_plate (str): The number plate of the vehicle.
        """

        # Check if there are any defaulted values
        if len(self.defaulted_values) > 0:
            # Combine the failed values into a string and add it to the errors
            values = ", ".join(self.defaulted_values)
            self.errors["defaulted_values"][number_plate] = f"De volgende kolommen zijn vervangen door standaardwaardes: {values}" 

            # Empty the defaulted values list
            self.defaulted_values = []