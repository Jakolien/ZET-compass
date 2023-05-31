from data_objects.ScenarioYear import ScenarioYear
from data_objects.Vehicle import Vehicle
from excel_interfaces.AbstractExcelInterface import AbstractExcelInterface
from exceptions import NoExcelFileFound, NoPANTEIAModelFound
from os.path import isfile
from utility_functions import convert_cooled_boolean


class PANTEIAInterface(AbstractExcelInterface):

    PANTEIA_model_path: str = None
    ondernemers_module_tab_name: str = "TCO module ondernemers"
    beleidsmakers_module_tab_name: str = "TCO module beleidsmakers"
    ondernemers_calc_tab_name: str = "ondernemers_calc"
    beleidsmakers_calc_tab_name: str = "beleidsmakers_calc"
    model_parameters_tab_name: str = "Model parameters"
    default_electric_lifespan: int = 7
    default_diesel_lifespan: int = 7

    def __init__(self):

        """Initialises an interface for a PANTEIA model.
        This interface can read from the file, but won't actually change it.
        It simulates the Excel file in memory, so "changing" a value only edits memory.

        :raise NoPANTEIAModelFound: Raised if the PANTEIA model can't be found or initialised.

        :return: An instance of PANTEIAInterface.
        :rtype: PANTEIAInterface
        """

        self.PANTEIA_model_path = "./PANTEIA_TCO_model.xlsm"

        # Check if template model exists
        PANTEIA_model_found = isfile(self.PANTEIA_model_path)
        if not PANTEIA_model_found:
            raise NoPANTEIAModelFound

        # Initiate the Excel model
        try:
            super().__init__(self.PANTEIA_model_path)
        except NoExcelFileFound:
            raise NoPANTEIAModelFound

        # Reset values before starting
        self.reset_values()

    def reset_values(self):

        """Resets the cell values to the default.

        :return: Nothing
        :rtype: None
        """

        self.reset_ondernemers_worksheet()
        self.reset_beleidsmakers_worksheet()
        self.reset_model_parameters_worksheet()

    def reset_ondernemers_worksheet(self):

        """Resets the cell values of the ondernemers worksheet to the default.

        :return: Nothing
        :rtype: None
        """

        # Reset mileage, productive hours and costs of repairs
        self.set_cell_value(self.ondernemers_module_tab_name, "B14", 35000)
        self.set_cell_value(self.ondernemers_module_tab_name, "C28", 26000)

        self.set_cell_value(self.ondernemers_module_tab_name, "B29", 5000)
        self.set_cell_value(self.ondernemers_module_tab_name, "C29", 1500)

        self.set_cell_value(self.ondernemers_module_tab_name, "B13", "niet gekoeld")
        self.set_cell_value(self.ondernemers_module_tab_name, "B15", "grijs")

        # Reset fuel and energy price
        self.set_cell_value(self.ondernemers_module_tab_name, "B21", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "B22", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "B23", None)

        # Reset lifespan
        self.set_cell_value(self.ondernemers_module_tab_name, "B26", 7)
        self.set_cell_value(self.ondernemers_module_tab_name, "C26", 7)

        # Reset residual value
        self.set_cell_value(self.ondernemers_module_tab_name, "B27", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "C27", None)

        # Reset stillstand
        self.set_cell_value(self.ondernemers_module_tab_name, "B30", 5)
        self.set_cell_value(self.ondernemers_module_tab_name, "C30", 1)

        # Reset residual debt
        self.set_cell_value(self.ondernemers_module_tab_name, "B31", 0)
        self.set_cell_value(self.ondernemers_module_tab_name, "C31", 0)

        # Reset battery and charging
        self.set_cell_value(self.ondernemers_module_tab_name, "E12", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E13", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E14", 150)
        self.set_cell_value(self.ondernemers_module_tab_name, "E15", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E16", None)

        # Reset vehicle price and subsidies
        self.set_cell_value(self.ondernemers_module_tab_name, "E21", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E22", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E23", None)

        # Reset charging prices and subsidies
        self.set_cell_value(self.ondernemers_module_tab_name, "E27", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E28", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E29", None)

        self.set_cell_value(self.beleidsmakers_module_tab_name, "B29", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B30", None)

        # Reset fuel and distance taxes
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E24", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E29", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E30", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E32", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E34", None)

        # Reset road taxes 
        self.set_cell_value(self.ondernemers_module_tab_name, "C56", 0)
        self.set_cell_value(self.ondernemers_module_tab_name, "D56", 0)

    def reset_beleidsmakers_worksheet(self):

        """Resets the cell values of the beleidsmakers worksheet to the default.

        :return: Nothing
        :rtype: None
        """

        # Reset mileage, productive hours and costs of repairs
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B14", 35000)
        self.set_cell_value(self.ondernemers_module_tab_name, "C28", 2600)

        self.set_cell_value(self.beleidsmakers_module_tab_name, "B13", "niet gekoeld")
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B15", "grijs")

        # Reset fuel price - ondernemers
        self.set_cell_value(self.ondernemers_module_tab_name, "B21", None)

        # Reset electric price
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B34", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B35", None)

        # Reset levensduur
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E13", 7)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "F13", 7)

        # Reset restwaarde
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E14", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "F14", None)

        # Reset battery and charging
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E16", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "F17", None)

        # Reset vehicle price and subsidies
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B24", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B25", None)

        # Reset charging prices and subsidies - beleidsmakers and ondernemers
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B29", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "B30", None)

        self.set_cell_value(self.ondernemers_module_tab_name, "E27", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E28", None)
        self.set_cell_value(self.ondernemers_module_tab_name, "E29", None)

        # Reset fuel and distance taxes
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E24", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E29", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E30", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E32", None)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E34", None)

    def reset_model_parameters_worksheet(self):

        """Resets the cell values of the model parameters worksheet to the default.

        :return: Nothing
        :rtype: None
        """

        # Reset vehicle price EV (first 4 not verified)
        self.set_cell_value(self.model_parameters_tab_name, "E4", 30000)
        self.set_cell_value(self.model_parameters_tab_name, "E5", 36000)
        self.set_cell_value(self.model_parameters_tab_name, "E6", 68000)
        self.set_cell_value(self.model_parameters_tab_name, "E7", 66380)
        self.set_cell_value(self.model_parameters_tab_name, "E8", 157000)
        self.set_cell_value(self.model_parameters_tab_name, "E9", 267500)
        self.set_cell_value(self.model_parameters_tab_name, "E10", 300000)

        # Reset kWh
        self.set_cell_value(self.model_parameters_tab_name, "D4", 40)
        self.set_cell_value(self.model_parameters_tab_name, "D5", 60)
        self.set_cell_value(self.model_parameters_tab_name, "D6", 90)
        self.set_cell_value(self.model_parameters_tab_name, "D7", 70)
        self.set_cell_value(self.model_parameters_tab_name, "D8", 82.8)
        self.set_cell_value(self.model_parameters_tab_name, "D9", 250)
        self.set_cell_value(self.model_parameters_tab_name, "D10", 275)

        # Reset vehicle price DV
        self.set_cell_value(self.model_parameters_tab_name, "E14", 11760)
        self.set_cell_value(self.model_parameters_tab_name, "E15", 17195)
        self.set_cell_value(self.model_parameters_tab_name, "E16", 24042)
        self.set_cell_value(self.model_parameters_tab_name, "E17", 23620)
        self.set_cell_value(self.model_parameters_tab_name, "E18", 62500)
        self.set_cell_value(self.model_parameters_tab_name, "E19", 115000)
        self.set_cell_value(self.model_parameters_tab_name, "E20", 144500)

        # Reset DV efficiency
        self.set_cell_value(self.model_parameters_tab_name, "I14", 0.057)
        self.set_cell_value(self.model_parameters_tab_name, "I15", 0.077)
        self.set_cell_value(self.model_parameters_tab_name, "I16", 0.084)
        self.set_cell_value(self.model_parameters_tab_name, "I17", 0.12)
        self.set_cell_value(self.model_parameters_tab_name, "I18", 0.102)
        self.set_cell_value(self.model_parameters_tab_name, "I19", 0.209)
        self.set_cell_value(self.model_parameters_tab_name, "I20", 0.318)

        # Reset EV efficiency
        self.set_cell_value(self.model_parameters_tab_name, "G14", 0.15)
        self.set_cell_value(self.model_parameters_tab_name, "G15", 0.21)
        self.set_cell_value(self.model_parameters_tab_name, "G16", 0.25)
        self.set_cell_value(self.model_parameters_tab_name, "G17", 0.31)
        self.set_cell_value(self.model_parameters_tab_name, "G18", 0.75)      # 0.270
        self.set_cell_value(self.model_parameters_tab_name, "G19", 0.9)      # 0.531
        self.set_cell_value(self.model_parameters_tab_name, "G20", 1.25)     # 0.796

        # Reset Toll (first 4 not verified)
        self.set_cell_value(self.model_parameters_tab_name, "P14", 100)
        self.set_cell_value(self.model_parameters_tab_name, "P15", 100)
        self.set_cell_value(self.model_parameters_tab_name, "P16", 100)
        self.set_cell_value(self.model_parameters_tab_name, "P17", 100)
        self.set_cell_value(self.model_parameters_tab_name, "P18", 750)
        self.set_cell_value(self.model_parameters_tab_name, "P19", 750)
        self.set_cell_value(self.model_parameters_tab_name, "P20", 1250)

    def input_vehicle_data(self, vehicle: Vehicle):

        """Input the specified vehicle data into the model.

        :param vehicle: The vehicle that contains the input data.
        :type vehicle: Vehicle

        :return: Nothing
        :rtype: None
        """

        self.set_cell_value(self.ondernemers_module_tab_name, "B12", vehicle.type)
        self.set_cell_value(self.ondernemers_module_tab_name, "B13", convert_cooled_boolean(vehicle.is_cooled))
        self.set_cell_value(self.ondernemers_module_tab_name, "B14", vehicle.expected_total_distance_traveled_in_km)
        # Assume 10 hours per operational day
        self.set_cell_value(self.ondernemers_module_tab_name, "C28", vehicle.amount_of_operational_days * 10)
        self.set_cell_value(self.ondernemers_module_tab_name, "B26", vehicle.technological_lifespan)
        self.set_cell_value(self.ondernemers_module_tab_name, "C26", vehicle.technological_lifespan)
        self.set_cell_value(self.ondernemers_module_tab_name, "B15", vehicle.electricity_type)

        # Calculate driving range per day
        days_in_operation = int(self.get_cell_value(self.ondernemers_calc_tab_name, "B6"))
        expected_daily_distance = vehicle.expected_total_distance_traveled_in_km/days_in_operation
        # Select either the expected daily distance or the maximum daily distance, whichever is higher
        driving_range_per_day = max(expected_daily_distance, vehicle.maximum_daily_distance_in_km)
        self.set_cell_value(self.ondernemers_module_tab_name, "B16", driving_range_per_day)

    def get_technological_lifespan(self):

        """Get the technological lifespans.

        :return: A dictionary with the lifespans as integers.
        :rtype: dict
        """

        electric_lifespan = int(self.get_cell_value(self.ondernemers_module_tab_name, "B26"))
        diesel_lifespan = int(self.get_cell_value(self.ondernemers_module_tab_name, "C26"))

        return {
            "electric": electric_lifespan,
            "diesel": diesel_lifespan
        }

    def reset_technological_lifespan(self):

        """Reset the technological lifespans to the default.

        :return: Nothing
        :rtype: None
        """

        self.set_cell_value(self.ondernemers_module_tab_name, "B26", self.default_electric_lifespan)
        self.set_cell_value(self.ondernemers_module_tab_name, "C26", self.default_diesel_lifespan)

    def set_ZE_costs(self, scenario_data: ScenarioYear):

        """Set the tax/fine for driving a diesel vehicle in a Zero Emission zone.

        :param scenario_data: The data for the current scenario.
        :type scenario_data: ScenarioYear

        :return: Nothing
        :rtype: None
        """

        self.set_cell_value(self.beleidsmakers_module_tab_name,
                            "E32",
                            scenario_data.fixed_ZE_vehicle_tax_in_euro_per_year)

    def reset_ZE_costs(self):

        """Reset the tax/fine for driving a diesel vehicle in a Zero Emission zone to the default.

        :return: Nothing
        :rtype: None
        """

        self.set_cell_value(self.beleidsmakers_module_tab_name, "E32", 0)

    def get_error_in_variable_costs(self, current_fuel_type: str):
        if current_fuel_type.capitalize() == "Diesel":
            error_in_brandstof = self.get_cell_value(self.ondernemers_module_tab_name, "B14")*self.get_cell_value(self.ondernemers_module_tab_name, "B65") -  self.get_cell_value(self.ondernemers_module_tab_name, "E65")
            error_in_banden = self.get_cell_value(self.ondernemers_module_tab_name, "B14")*self.get_cell_value(self.ondernemers_module_tab_name, "B68") -  self.get_cell_value(self.ondernemers_module_tab_name, "E68")
            error_in_onderhoud = self.get_cell_value(self.ondernemers_module_tab_name, "B14")*self.get_cell_value(self.ondernemers_module_tab_name, "B69") -  self.get_cell_value(self.ondernemers_module_tab_name, "E69")
        else:
            error_in_brandstof = self.get_cell_value(self.ondernemers_module_tab_name, "B14") * self.get_cell_value(self.ondernemers_module_tab_name, "B65") - self.get_cell_value(self.ondernemers_module_tab_name, "E65")
            error_in_banden = self.get_cell_value(self.ondernemers_module_tab_name, "B14") * self.get_cell_value(self.ondernemers_module_tab_name, "B68") - self.get_cell_value(self.ondernemers_module_tab_name, "E68")
            error_in_onderhoud = self.get_cell_value(self.ondernemers_module_tab_name, "B14") * self.get_cell_value(self.ondernemers_module_tab_name, "B69") - self.get_cell_value(self.ondernemers_module_tab_name, "E69")

        return error_in_brandstof + error_in_banden + error_in_onderhoud

    def get_error_in_total_costs(self, current_fuel_type: str):
        return self.get_error_in_variable_costs(current_fuel_type) + self.get_error_in_driver_costs(current_fuel_type)

    def get_error_in_co2_emissions(self, current_fuel_type: str, vehicle_index: int):
        liters = self.get_cell_value(self.ondernemers_module_tab_name, "B14") * self.get_cell_value(self.model_parameters_tab_name, "I" + str(14 + vehicle_index)) / 1000

        g_per_liters = self.get_cell_value(self.model_parameters_tab_name, "B" + str(77 + vehicle_index)) / 1000
        gram_co2 = g_per_liters * liters
        return gram_co2 - self.get_cell_value(self.ondernemers_module_tab_name, "E49")

    def get_error_in_driver_costs(self, current_fuel_type: str):
        if current_fuel_type.capitalize() == "Diesel":
            error_in_uurloon = self.get_cell_value(self.ondernemers_module_tab_name, "B92") * self.get_cell_value(self.ondernemers_module_tab_name, "C28") - self.get_cell_value(self.ondernemers_module_tab_name, "E92")
            error_in_verblijfskosten = self.get_cell_value(self.ondernemers_module_tab_name, "B93") * self.get_cell_value(self.ondernemers_module_tab_name, "C28") - self.get_cell_value(self.ondernemers_module_tab_name, "E93")
            error_in_overig = self.get_cell_value(self.ondernemers_module_tab_name, "B94") * self.get_cell_value(self.ondernemers_module_tab_name, "C28") - self.get_cell_value(self.ondernemers_module_tab_name, "E94")
        else:
            error_in_uurloon = self.get_cell_value(self.ondernemers_module_tab_name, "B92")*self.get_cell_value(self.ondernemers_module_tab_name, "C28") -  self.get_cell_value(self.ondernemers_module_tab_name, "E92")
            error_in_verblijfskosten = self.get_cell_value(self.ondernemers_module_tab_name, "B93")*self.get_cell_value(self.ondernemers_module_tab_name, "C28") -  self.get_cell_value(self.ondernemers_module_tab_name, "E93")
            error_in_overig = self.get_cell_value(self.ondernemers_module_tab_name, "B94")*self.get_cell_value(self.ondernemers_module_tab_name, "C28") -  self.get_cell_value(self.ondernemers_module_tab_name, "E94")
        return error_in_uurloon + error_in_verblijfskosten + error_in_overig

    def update_fixed_parameters(self,
                                vehicle_lifespan: int,
                                vehicle_index: int,
                                charging_time_depot: int,
                                charging_time_public: int,
                                tax_percentage: float,
                                scenario_data: ScenarioYear,
                                future_scenario_data: ScenarioYear):

        """Update the fixed parameters in the model.

        :param vehicle_lifespan: The current lifespan of the vehicle in years.
        :type vehicle_lifespan: int
        :param vehicle_index: The index of the current vehicle type
        :type vehicle_index : int
        :param charging_time_depot: The time charging on the depot.
        :type charging_time_depot: int
        :param charging_time_public: The time charging in public.
        :type charging_time_public: int
        :param tax_percentage: The tax percentage of a company.
        :type tax_percentage: float
        :param scenario_data: The data for the current scenario.
        :type scenario_data: ScenarioYear
        :param future_scenario_data: The data for the current scenario in the future
        :type future_scenario_data: ScenarioYear

        :return: Nothing
        :rtype: None
        """

        # TODO Add capacity diesel (increases too)
        # Change prices and efficiency in model parameters
        self.set_cell_value(self.model_parameters_tab_name, "E" + str(4 + vehicle_index), scenario_data.electric_price_in_euro)
        self.set_cell_value(self.model_parameters_tab_name, "E" + str(14 + vehicle_index), scenario_data.diesel_price_in_euro)
        self.set_cell_value(self.model_parameters_tab_name, "D" + str(4 + vehicle_index), scenario_data.capacity_in_kWh)
        self.set_cell_value(self.model_parameters_tab_name, "G" + str(14 + vehicle_index), scenario_data.efficiency_electricity_in_kWh_per_km)
        self.set_cell_value(self.model_parameters_tab_name, "I" + str(14 + vehicle_index), scenario_data.efficiency_diesel_in_liter_per_km)

        # Subsidies and investment deduction
        self.set_cell_value(self.ondernemers_module_tab_name, "E23", scenario_data.subsidies_EV_in_euro)
        investment_deduction = tax_percentage * (scenario_data.MIA_in_euro_per_lifespan + scenario_data.VAMIL_in_euro_per_lifespan)
        self.set_cell_value(self.ondernemers_module_tab_name, "E22", investment_deduction)

        # Reset Residual debt
        self.set_cell_value(self.ondernemers_module_tab_name, "B31", 0)
        self.set_cell_value(self.ondernemers_module_tab_name, "C31", 0)

        # Residual value (original price * residual percentage)
        original_electric_price = scenario_data.electric_price_in_euro
        original_diesel_price = scenario_data.diesel_price_in_euro
        residual_percentage_electric = getattr(future_scenario_data, f"residual_value_EV_year_{vehicle_lifespan}_in_percentage")
        residual_percentage_diesel = getattr(future_scenario_data, f"residual_value_diesel_year_{vehicle_lifespan}_in_percentage")
        residual_value_electric = original_electric_price * residual_percentage_electric
        residual_value_diesel = original_diesel_price * residual_percentage_diesel

        self.set_cell_value(self.ondernemers_module_tab_name, "B27", residual_value_electric)
        self.set_cell_value(self.ondernemers_module_tab_name, "C27", residual_value_diesel)

        # TODO Check Excel for calculation charging system per year (now based on life time vehicle)
        # Charging system
        self.set_cell_value(self.ondernemers_module_tab_name, "E27", scenario_data.gross_purchase_cost_charging_system_in_euro)
        self.set_cell_value(self.ondernemers_module_tab_name, "E28", scenario_data.gross_installation_cost_charging_system_in_euro)

        # Charging capacity depot
        self.set_cell_value(self.ondernemers_module_tab_name, "E13", scenario_data.charging_capacity_charging_pole_on_depot)

        # Charging time
        self.set_cell_value(self.ondernemers_module_tab_name, "E15", charging_time_depot)
        self.set_cell_value(self.ondernemers_module_tab_name, "E16", charging_time_public)

        # Days standing still
        self.set_cell_value(self.ondernemers_module_tab_name, "B30", scenario_data.standstil_EV_in_days)
        self.set_cell_value(self.ondernemers_module_tab_name, "C30", 1)

    def update_variable_parameters(self, scenario_data: ScenarioYear):

        """Update the variable parameters in the model.

        :param scenario_data: The data for the current scenario.
        :type scenario_data: ScenarioYear

        :return: Nothing
        :rtype: None
        """

        # Repair costs
        self.set_cell_value(self.ondernemers_module_tab_name, "B29", scenario_data.repair_costs_EV_euro_per_year)
        self.set_cell_value(self.ondernemers_module_tab_name, "C29", 1500)

        # TODO Add Maintenance costs

        # CO2 price
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E34", scenario_data.CO2_price_in_euro_per_ton)

        # Fuel prices
        self.set_cell_value(self.ondernemers_module_tab_name, "B21", scenario_data.fuel_price_diesel_excluding_tax_in_euro_per_liter)
        self.set_cell_value(self.ondernemers_module_tab_name, "B22", scenario_data.electricity_price_private_excluding_tax_in_euro_per_kWh)
        self.set_cell_value(self.ondernemers_module_tab_name, "B23", scenario_data.electricity_price_public_excluding_tax_in_euro_per_kWh)
        self.set_cell_value(self.beleidsmakers_module_tab_name, "E24", scenario_data.change_in_excise_duty_diesel_in_percentage)

        # Vehicle tax (Diesel stays constant)
        self.set_cell_value(self.ondernemers_module_tab_name, "C56", scenario_data.vehicle_tax_electric_in_euro_per_year)
        self.set_cell_value(self.ondernemers_module_tab_name, "D56", scenario_data.vehicle_tax_electric_in_euro_per_year)
        # self.set_cell_value(self.ondernemers_module_tab_name,. "E56", scenario_datavehicle_tax_diesel_in_euro_per_year)

        # Charging capacity
        self.set_cell_value(self.ondernemers_module_tab_name, "E14", scenario_data.charging_capacity_external_charging_pole)

    # TODO Find a way to add this, without being in fixed parameters (so that it will be smeared over the lifespan)
    def update_price_electric_vehicle(self,
                                vehicle_index: int,
                                additional_price: int
                                ):

        """Ass a workaround, add residual debt to vehicle price.


        :param additional_price: The residual debt from last vehicle is added here
        :type additional_price: int
        :param vehicle_index: The index of the current vehicle type
        :type vehicle_index : int

        :return: Nothing
        :rtype: None
        """

        reparatiekosten = self.get_cell_value(self.ondernemers_module_tab_name, "B29")
        self.set_cell_value(self.ondernemers_module_tab_name, "B29", reparatiekosten + additional_price)

    def increase_maintenance_factor(self, fuel_type: str, yearly_increase_factor: float):

        """Increases the maintenance cost by a specified factor.

        :param fuel_type: The fuel type of the vehicle.
        :type fuel_type: str
        :param yearly_increase_factor: The factor by which the costs should increase.
        :type yearly_increase_factor: float

        :return: Nothing
        :rtype: None
        """

        if fuel_type.capitalize() == "Diesel":
            cost_of_repairs = int(self.get_cell_value(self.ondernemers_module_tab_name, "C29"))
            days_standing_still = float(self.get_cell_value(self.ondernemers_module_tab_name, "C30"))
            self.set_cell_value(self.ondernemers_module_tab_name, "C29", cost_of_repairs * yearly_increase_factor)
            self.set_cell_value(self.ondernemers_module_tab_name, "C30", days_standing_still * yearly_increase_factor)
        else:
            cost_of_repairs = int(self.get_cell_value(self.ondernemers_module_tab_name, "B29"))
            days_standing_still = float(self.get_cell_value(self.ondernemers_module_tab_name, "B30"))
            self.set_cell_value(self.ondernemers_module_tab_name, "B29", cost_of_repairs * yearly_increase_factor)
            self.set_cell_value(self.ondernemers_module_tab_name, "B30", days_standing_still * yearly_increase_factor)

    def decrease_yearly_depreciation_costs(self, fuel_type: str, vehicle_age: int):

        """Decreases the yearly depreciation cost because vehicle is already paid off.

        :param current_fuel_type: The vehicles current fuel type.
        :type current_fuel_type: str
        :param current_vehicle_age: The current age of the vehicle.
        :type current_vehicle_age: int

        :return: Nothing
        :rtype: None
        """

        # TODO Make new function to compute residual values
        # Calculate yearly depreciation costs
        if 0 < vehicle_age < 16:
            vehicle_price = self.get_cell_value(self.ondernemers_calc_tab_name, "I39")
            old_percentage_vehicle = self.get_cell_value(self.model_parameters_tab_name, "B" + str(57 + int(vehicle_age)))
            new_percentage_vehicle = self.get_cell_value(self.model_parameters_tab_name,"B" + str(58 + int(vehicle_age)))
            difference = vehicle_price * (old_percentage_vehicle - new_percentage_vehicle)
        else:
            return ValueError

        # update depreciation costs and life span
        if fuel_type.capitalize() == "Diesel":
            self.set_cell_value(self.ondernemers_module_tab_name,"B31",1)
            self.set_cell_value(self.ondernemers_module_tab_name,"C31",difference)
        else:
            return ValueError

    def reset_yearly_depreciation_costs(self):

        """Resets the yearly depreciation cost because vehicle is already paid off.

        :return: Nothing
        :rtype: None
        """

        self.set_cell_value(self.ondernemers_module_tab_name,"B31",0)
        self.set_cell_value(self.ondernemers_module_tab_name,"C31",0)

    def set_ZE_costs(self, scenario_data: ScenarioYear):

        """Adds extra costs for driving in a ZE-zone with a Diesel vehicle

        :param scenario_data: The data for the current scenario.
        :type scenario_data: ScenarioYear

        :return: Nothing
        :rtype: None
        """

        self.set_cell_value(self.beleidsmakers_module_tab_name, "E32", scenario_data.fixed_ZE_vehicle_tax_in_euro_per_year)

    def reset_ZE_costs(self):

        """Reset extra costs for driving in a ZE-zone with a Diesel vehicle to zero

        :param scenario_data: The data for the current scenario.
        :type scenario_data: ScenarioYear

        :return: Nothing
        :rtype: None
        """

        self.set_cell_value(self.beleidsmakers_module_tab_name, "E32", 0)

    def calculate_residual_debt(self, lifespan: int, vehicle_age: int):

        """Decreases the yearly depreciation cost because vehicle is already paid off.

        :param current_lifespan: The current lifespan of the vehicle.
        :type current_lifespan: int
        :param current_vehicle_age: The current age of the vehicle.
        :type current_vehicle_age: int

        :return: residual debt
        :rtype: int
        """

        # TODO Make new function to compute residual values
        # calculate residual debt
        if 0 <= vehicle_age <= 15 and 0 <= lifespan <= 15:
            vehicle_price = self.get_cell_value(self.ondernemers_calc_tab_name, "I39")
            old_percentage_vehicle = self.get_cell_value(self.model_parameters_tab_name, "B" + str(58 + int(lifespan)))
            new_percentage_vehicle = self.get_cell_value(self.model_parameters_tab_name, "B" + str(58 + int(vehicle_age)))
            old_residual_value = vehicle_price * old_percentage_vehicle
            new_residual_value = vehicle_price * new_percentage_vehicle     # TODO Does not change in time here
            residual_debt = vehicle_price - new_residual_value - (vehicle_price - old_residual_value) / lifespan * vehicle_age  # positive if residual debt open

        return max(0, int(residual_debt))

    def is_optimal_mix_valid(self):

        """Gets whether using an optimal mix of charging is possible.

        :return: Whether optimal mix is possible.
        :rtype: bool
        """

        is_scenario_valid = self.get_cell_value(self.ondernemers_module_tab_name, "D35")
        return is_scenario_valid.lower() == "scenario valid"

    def is_exclusive_home_loading_valid(self):

        """Gets whether exclusively loading from home/depot is possible.

        :return: Whether exclusive home loading is possible.
        :rtype bool
        """

        is_scenario_valid = self.get_cell_value(self.ondernemers_module_tab_name, "C35")
        return is_scenario_valid.lower() == "scenario valid"

    def get_total_TCO_cost_depot_charging(self):

        """Get the total TCO costs for exclusively charging at depot.

        :return: The total TCO cost. Or false if value can't be retrieved.
        :rtype: float or False
        """

        try:
            return float(self.get_cell_value(self.ondernemers_module_tab_name, "C44"))
        except ValueError:
            return False

    def get_total_TCO_cost_optimal_mix(self):

        """Get the total TCO costs for optimal mix. Or false if value can't be retrieved.

        :return: The total TCO cost.
        :rtype: float or False
        """

        try:
            return float(self.get_cell_value(self.ondernemers_module_tab_name, "D44"))
        except ValueError:
            return False

    def get_total_TCO_cost_diesel(self):

        """Get the total TCO costs for diesel. Or false if value can't be retrieved.

        :return: The total TCO cost.
        :rtype: float or False
        """

        try:
            return float(self.get_cell_value(self.ondernemers_module_tab_name, "E44"))
        except ValueError:
            return False

    def get_TCO_diesel(self, transition_year: int = 0):

        """Gets the TCO values for a diesel vehicle.

        :param transition_year: The transition year.
        :type transition_year: int

        :return: The TCO values.
        :rtype: dict
        """

        tco = int(self.get_cell_value(self.ondernemers_module_tab_name, 'E44'))
        fixed_vehicle_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'E62'))
        variable_vehicle_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'E75'))
        write_off_costs_vehicle = int(self.get_cell_value(self.ondernemers_module_tab_name, 'E80'))
        write_off_costs_charging_system = int(self.get_cell_value(self.ondernemers_module_tab_name, 'E85'))
        driver_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'E95'))
        costs_public_charging = 0
        CO2_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'E49'))
        particulate_matter_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'E50'))
        nitrogen_oxide_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'E51'))
        kWh_charged_on_depot = 0.0
        kWh_charged_in_public = 0.0
        charging_time_depot = 0.0
        charging_time_public = 0.0

        return self.create_TCO_result_dictionary(tco,
                                                 fixed_vehicle_costs,
                                                 variable_vehicle_costs,
                                                 write_off_costs_vehicle,
                                                 write_off_costs_charging_system,
                                                 driver_costs,
                                                 costs_public_charging,
                                                 CO2_emissions,
                                                 particulate_matter_emissions,
                                                 nitrogen_oxide_emissions,
                                                 kWh_charged_on_depot,
                                                 kWh_charged_in_public,
                                                 charging_time_depot,
                                                 charging_time_public,
                                                 transition_year)

    def get_TCO_electric(self,
                         is_exclusive_charging_at_depot_possible: bool = True,
                         transition_year: int = 1):

        """Gets the TCO values for an electric vehicle.

        :param is_exclusive_charging_at_depot_possible: Whether exclusively charging at the depot is possible.
        :type is_exclusive_charging_at_depot_possible: bool
        :param transition_year: The transition year.
        :type transition_year: int

        :return: The TCO values.
        :rtype: dict
        """

        if is_exclusive_charging_at_depot_possible:
            tco = int(self.get_cell_value(self.ondernemers_module_tab_name, 'C44'))
            fixed_vehicle_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'C62'))
            variable_vehicle_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'C75'))
            write_off_costs_vehicle = int(self.get_cell_value(self.ondernemers_module_tab_name, 'C80'))
            write_off_costs_charging_system = int(self.get_cell_value(self.ondernemers_module_tab_name, 'C85'))
            driver_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'C95'))
            costs_public_charging = 0
            CO2_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'C49'))
            particulate_matter_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'C50'))
            nitrogen_oxide_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'C51'))
            kWh_charged_on_depot = float(self.get_cell_value(self.ondernemers_calc_tab_name, "B35"))
            kWh_charged_in_public = 0.0
            charging_time_depot = float(self.get_cell_value(self.ondernemers_calc_tab_name, "B32"))
            charging_time_public = 0.0
        else:
            tco = int(self.get_cell_value(self.ondernemers_module_tab_name, 'D44'))
            fixed_vehicle_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'D62'))
            variable_vehicle_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'D75'))
            write_off_costs_vehicle = int(self.get_cell_value(self.ondernemers_module_tab_name, 'D80'))
            write_off_costs_charging_system = int(self.get_cell_value(self.ondernemers_module_tab_name, 'D85'))
            driver_costs = int(self.get_cell_value(self.ondernemers_module_tab_name, 'D95'))
            costs_public_charging = max(0,driver_costs - int(self.get_cell_value(self.ondernemers_module_tab_name, 'C95'))) + 144 # TODO 144 euro are costs for abonnement fastned, change this in scenarios
            CO2_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'D49'))
            particulate_matter_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'D50'))
            nitrogen_oxide_emissions = float(self.get_cell_value(self.ondernemers_module_tab_name, 'D51'))
            kWh_charged_on_depot = float(self.get_cell_value(self.ondernemers_calc_tab_name, "C35"))
            kWh_charged_in_public = float(self.get_cell_value(self.ondernemers_calc_tab_name, "C47"))
            charging_time_depot = float(self.get_cell_value(self.ondernemers_calc_tab_name, "C32"))
            charging_time_public = float(self.get_cell_value(self.ondernemers_calc_tab_name, "C48"))

        return self.create_TCO_result_dictionary(tco,
                                                 fixed_vehicle_costs,
                                                 variable_vehicle_costs,
                                                 write_off_costs_vehicle,
                                                 write_off_costs_charging_system,
                                                 driver_costs,
                                                 costs_public_charging,
                                                 CO2_emissions,
                                                 particulate_matter_emissions,
                                                 nitrogen_oxide_emissions,
                                                 kWh_charged_on_depot,
                                                 kWh_charged_in_public,
                                                 charging_time_depot,
                                                 charging_time_public,
                                                 transition_year)

    def create_TCO_result_dictionary(self,
                                     tco: int,
                                     fixed_vehicle_costs: int,
                                     variable_vehicle_costs: int,
                                     write_off_costs_vehicle: int,
                                     write_off_costs_charging_system: int,
                                     driver_costs: int,
                                     costs_public_charging: int,
                                     CO2_emissions: float,
                                     particulate_matter_emissions: float,
                                     nitrogen_oxide_emissions: float,
                                     kWh_charged_on_depot: float,
                                     kWh_charged_in_public: float,
                                     charging_time_depot: float,
                                     charging_time_public: float,
                                     transition_year: int):

        """Format the TCO results as a dictionary.

        :param tco: The total TCO costs.
        :type tco: int
        :param fixed_vehicle_costs: The fixed vehicle costs.
        :type fixed_vehicle_costs: int
        :param variable_vehicle_costs: The total variable costs.
        :type variable_vehicle_costs: int
        :param write_off_costs_vehicle: The total vehicle write off costs.
        :type write_off_costs_vehicle: int
        :param write_off_costs_charging_system: The total charging system write off costs.
        :type write_off_costs_charging_system: int
        :param driver_costs: The total driver/chauffeur costs.
        :type driver_costs: int
        :param costs_public_charging: The total costs for public charging.
        :type costs_public_charging: int
        :param CO2_emissions: The total CO2 emissions.
        :type CO2_emissions: float
        :param particulate_matter_emissions: The total particulate matter emissions.
        :type particulate_matter_emissions: float
        :param nitrogen_oxide_emissions: The total nitrogen oxide emissions.
        :type nitrogen_oxide_emissions: float
        :param kWh_charged_on_depot: The total kWh charged on the depot.
        :type kWh_charged_on_depot: float
        :param kWh_charged_in_public: The total kWh charged in public.
        :type kWh_charged_in_public: float
        :param charging_time_depot: The total charging time on the depot.
        :type charging_time_depot: float
        :param charging_time_public: The total charging time in public.
        :type charging_time_public: float
        :param transition_year: The transition year.
        :type transition_year: int

        :return: The formatted TCO results.
        :rtype: dict
        """

        return {
            "tco": tco,
            "fixed_vehicle_costs": fixed_vehicle_costs,
            "variable_vehicle_costs": variable_vehicle_costs,
            "write_off_costs_vehicle": write_off_costs_vehicle,
            "write_off_costs_charging_system": write_off_costs_charging_system,
            "driver_costs": driver_costs,
            "costs_public_charging": costs_public_charging,
            "CO2_emissions": CO2_emissions,
            "particulate_matter_emissions": particulate_matter_emissions,
            "nitrogen_oxide_emissions": nitrogen_oxide_emissions,
            "kWh_charged_on_depot": kWh_charged_on_depot,
            "kWh_charged_in_public": kWh_charged_in_public,
            "charging_time_depot": charging_time_depot,
            "charging_time_public": charging_time_public,
            "transition_year": transition_year
        }
