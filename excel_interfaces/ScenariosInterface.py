from excel_interfaces.AbstractExcelInterface import AbstractExcelInterface
from exceptions import NoExcelFileFound, NoScenarioDataFound
from data_objects.Scenario import Scenario
from data_objects.ScenarioYear import ScenarioYear
from utility_functions import get_next_excel_column


class ScenariosInterface(AbstractExcelInterface):

    valid_scenario_names: tuple = (
        "laag",
        "midden",
        "hoog"
    )
    valid_scenario_sheet_names: tuple = (
        "laag 1",
        "laag 2",
        "laag 3",
        "laag 4",
        "laag 5",
        "laag 6",
        "laag 7",
        "midden 1",
        "midden 2",
        "midden 3",
        "midden 4",
        "midden 5",
        "midden 6",
        "midden 7",
        "hoog 1",
        "hoog 2",
        "hoog 3",
        "hoog 4",
        "hoog 5",
        "hoog 6",
        "hoog 7",
    )
    scenarios: dict = {}

    def __init__(self, path_to_scenario_data):

        """Initialises an interface for a scenarios data file.
        This interface can read from the file, but won't actually change it.
        It simulates the Excel file in memory, so "changing" a value only edits memory.

        :param path_to_scenario_data: The path to the scenario data file that the interface will interact with.
        :type path_to_scenario_data: str

        :raise NoScenarioDataFound: Raised if the scenario data file can't be found or initialised.

        :return: An instance of ScenarioInterface.
        :rtype: ScenarioInterface
        """

        try:
            super().__init__(path_to_scenario_data)
        except NoExcelFileFound:
            raise NoScenarioDataFound

        # Read scenario data
        for scenario_sheet_name in self.valid_scenario_sheet_names:

            # Split sheet name into scenario and vehicle type
            scenario_type, vehicle_type = scenario_sheet_name.split(" ")

            # Check if Worksheet exists
            try:
                if self.get_cell_value(scenario_sheet_name, "A1") is not None:
                    index_column = "B"
                    years = {}
                    reading_scenario_data = True

                    last_energy_subsidy: int = 0
                    last_ZE_vehicle_tax: int = 0
                    last_difference_truck_toll_tax: int = 0
                    last_subsidy_charging_system: int = 0
                    while reading_scenario_data:
                        year = self.get_cell_value(scenario_sheet_name, f"{index_column}1")

                        # If year is empty, stop searching
                        if year is None:
                            reading_scenario_data = False
                            continue

                        diesel_price_in_euro = self.get_cell_value(scenario_sheet_name, f"{index_column}2")
                        electric_price_in_euro = self.get_cell_value(scenario_sheet_name, f"{index_column}3")
                        capacity_in_kWh = self.get_cell_value(scenario_sheet_name, f"{index_column}4")
                        repair_costs_EV_euro_per_year = self.get_cell_value(scenario_sheet_name, f"{index_column}5")
                        maintenance_costs_EV_euro_per_km = self.get_cell_value(scenario_sheet_name, f"{index_column}6")
                        maintenance_costs_diesel_euro_per_km = self.get_cell_value(scenario_sheet_name, f"{index_column}7")
                        standstil_EV_in_days = self.get_cell_value(scenario_sheet_name, f"{index_column}8")
                        subsidies_EV_in_euro = self.get_cell_value(scenario_sheet_name, f"{index_column}9")
                        CO2_price_in_euro_per_ton = self.get_cell_value(scenario_sheet_name, f"{index_column}10")
                        efficiency_diesel_in_liter_per_km = self.get_cell_value(scenario_sheet_name, f"{index_column}11")
                        efficiency_electricity_in_kWh_per_km = self.get_cell_value(scenario_sheet_name, f"{index_column}12")
                        electricity_price_private_excluding_tax_in_euro_per_kWh = self.get_cell_value(scenario_sheet_name, f"{index_column}13")
                        electricity_price_public_excluding_tax_in_euro_per_kWh = self.get_cell_value(scenario_sheet_name, f"{index_column}14")
                        gross_purchase_cost_charging_system_in_euro = self.get_cell_value(scenario_sheet_name, f"{index_column}15")
                        gross_installation_cost_charging_system_in_euro = self.get_cell_value(scenario_sheet_name, f"{index_column}16")
                        fuel_price_diesel_excluding_tax_in_euro_per_liter = self.get_cell_value(scenario_sheet_name, f"{index_column}17")
                        change_in_excise_duty_diesel_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}18")
                        vehicle_tax_diesel_in_euro_per_year = self.get_cell_value(scenario_sheet_name, f"{index_column}19")
                        vehicle_tax_electric_in_euro_per_year = self.get_cell_value(scenario_sheet_name, f"{index_column}20")
                        MIA_in_euro_per_lifespan = self.get_cell_value(scenario_sheet_name, f"{index_column}21")
                        VAMIL_in_euro_per_lifespan = self.get_cell_value(scenario_sheet_name, f"{index_column}22")
                        energy_subsidy_in_euro_per_kWh = self.get_cell_value(scenario_sheet_name, f"{index_column}23")
                        fixed_ZE_vehicle_tax_in_euro_per_year = self.get_cell_value(scenario_sheet_name, f"{index_column}24")
                        difference_truck_toll_tax_in_euro_per_km = self.get_cell_value(scenario_sheet_name, f"{index_column}25")
                        subsidy_charging_system_installation_in_euro_per_installation = self.get_cell_value(scenario_sheet_name, f"{index_column}26")
                        residual_value_EV_year_1_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}27")
                        residual_value_EV_year_2_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}28")
                        residual_value_EV_year_3_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}29")
                        residual_value_EV_year_4_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}30")
                        residual_value_EV_year_5_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}31")
                        residual_value_EV_year_6_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}32")
                        residual_value_EV_year_7_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}33")
                        residual_value_EV_year_8_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}34")
                        residual_value_EV_year_9_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}35")
                        residual_value_EV_year_10_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}36")
                        residual_value_EV_year_11_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}37")
                        residual_value_EV_year_12_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}38")
                        residual_value_EV_year_13_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}39")
                        residual_value_EV_year_14_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}40")
                        residual_value_EV_year_15_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}41")
                        residual_value_diesel_year_1_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}42")
                        residual_value_diesel_year_2_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}43")
                        residual_value_diesel_year_3_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}44")
                        residual_value_diesel_year_4_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}45")
                        residual_value_diesel_year_5_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}46")
                        residual_value_diesel_year_6_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}47")
                        residual_value_diesel_year_7_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}48")
                        residual_value_diesel_year_8_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}49")
                        residual_value_diesel_year_9_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}50")
                        residual_value_diesel_year_10_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}51")
                        residual_value_diesel_year_11_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}52")
                        residual_value_diesel_year_12_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}53")
                        residual_value_diesel_year_13_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}54")
                        residual_value_diesel_year_14_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}55")
                        residual_value_diesel_year_15_in_percentage = self.get_cell_value(scenario_sheet_name, f"{index_column}56")
                        charging_capacity_external_charging_pole = self.get_cell_value(scenario_sheet_name, f"{index_column}57")
                        charging_capacity_charging_pole_on_depot = self.get_cell_value(scenario_sheet_name, f"{index_column}58")
                        needed_charging_capacity_depot = self.get_cell_value(scenario_sheet_name, f"{index_column}59")
                        needed_charging_capacity_in_transit = self.get_cell_value(scenario_sheet_name, f"{index_column}60")
                        AC37_at_home = self.get_cell_value(scenario_sheet_name, f"{index_column}61")
                        AC10_in_transit = self.get_cell_value(scenario_sheet_name, f"{index_column}62")
                        AC20_in_transit = self.get_cell_value(scenario_sheet_name, f"{index_column}63")
                        AC20_at_home = self.get_cell_value(scenario_sheet_name, f"{index_column}64")
                        FC50_in_transit = self.get_cell_value(scenario_sheet_name, f"{index_column}65")
                        FC50_at_home = self.get_cell_value(scenario_sheet_name, f"{index_column}66")
                        HPC150_in_transit = self.get_cell_value(scenario_sheet_name, f"{index_column}67")
                        HPC150_at_home = self.get_cell_value(scenario_sheet_name, f"{index_column}68")
                        HPC350_in_transit = self.get_cell_value(scenario_sheet_name, f"{index_column}69")
                        HPC350_at_home = self.get_cell_value(scenario_sheet_name, f"{index_column}70")

                        try:
                            scenario_data = ScenarioYear(
                                int(year),
                                float(diesel_price_in_euro),
                                float(electric_price_in_euro),
                                int(capacity_in_kWh),
                                float(repair_costs_EV_euro_per_year),
                                float(maintenance_costs_EV_euro_per_km),
                                float(maintenance_costs_diesel_euro_per_km),
                                float(standstil_EV_in_days),
                                float(subsidies_EV_in_euro),
                                float(CO2_price_in_euro_per_ton),
                                float(efficiency_diesel_in_liter_per_km),
                                float(efficiency_electricity_in_kWh_per_km),
                                float(electricity_price_private_excluding_tax_in_euro_per_kWh),
                                float(electricity_price_public_excluding_tax_in_euro_per_kWh),
                                float(gross_purchase_cost_charging_system_in_euro),
                                float(gross_installation_cost_charging_system_in_euro),
                                float(fuel_price_diesel_excluding_tax_in_euro_per_liter),
                                float(change_in_excise_duty_diesel_in_percentage),
                                float(vehicle_tax_diesel_in_euro_per_year),
                                float(vehicle_tax_electric_in_euro_per_year),
                                int(MIA_in_euro_per_lifespan),
                                int(VAMIL_in_euro_per_lifespan),
                                float(energy_subsidy_in_euro_per_kWh if energy_subsidy_in_euro_per_kWh
                                      else last_energy_subsidy),
                                float(fixed_ZE_vehicle_tax_in_euro_per_year if fixed_ZE_vehicle_tax_in_euro_per_year
                                      else last_ZE_vehicle_tax),
                                float(difference_truck_toll_tax_in_euro_per_km if difference_truck_toll_tax_in_euro_per_km
                                      else last_difference_truck_toll_tax),
                                float(subsidy_charging_system_installation_in_euro_per_installation
                                      if subsidy_charging_system_installation_in_euro_per_installation
                                      else last_subsidy_charging_system),
                                float(residual_value_EV_year_1_in_percentage),
                                float(residual_value_EV_year_2_in_percentage),
                                float(residual_value_EV_year_3_in_percentage),
                                float(residual_value_EV_year_4_in_percentage),
                                float(residual_value_EV_year_5_in_percentage),
                                float(residual_value_EV_year_6_in_percentage),
                                float(residual_value_EV_year_7_in_percentage),
                                float(residual_value_EV_year_8_in_percentage),
                                float(residual_value_EV_year_9_in_percentage),
                                float(residual_value_EV_year_10_in_percentage),
                                float(residual_value_EV_year_11_in_percentage),
                                float(residual_value_EV_year_12_in_percentage),
                                float(residual_value_EV_year_13_in_percentage),
                                float(residual_value_EV_year_14_in_percentage),
                                float(residual_value_EV_year_15_in_percentage),
                                float(residual_value_diesel_year_1_in_percentage),
                                float(residual_value_diesel_year_2_in_percentage),
                                float(residual_value_diesel_year_3_in_percentage),
                                float(residual_value_diesel_year_4_in_percentage),
                                float(residual_value_diesel_year_5_in_percentage),
                                float(residual_value_diesel_year_6_in_percentage),
                                float(residual_value_diesel_year_7_in_percentage),
                                float(residual_value_diesel_year_8_in_percentage),
                                float(residual_value_diesel_year_9_in_percentage),
                                float(residual_value_diesel_year_10_in_percentage),
                                float(residual_value_diesel_year_11_in_percentage),
                                float(residual_value_diesel_year_12_in_percentage),
                                float(residual_value_diesel_year_13_in_percentage),
                                float(residual_value_diesel_year_14_in_percentage),
                                float(residual_value_diesel_year_15_in_percentage),
                                float(charging_capacity_external_charging_pole),
                                float(charging_capacity_charging_pole_on_depot),
                                float(needed_charging_capacity_depot),
                                float(needed_charging_capacity_in_transit),
                                float(AC37_at_home),
                                float(AC10_in_transit),
                                float(AC20_in_transit),
                                float(AC20_at_home),
                                float(FC50_in_transit),
                                float(FC50_at_home),
                                float(HPC150_in_transit),
                                float(HPC150_at_home),
                                float(HPC350_in_transit),
                                float(HPC350_at_home)
                            )
                        except TypeError:
                            reading_scenario_data = False
                            continue

                        years[year] = scenario_data

                        # Increment column
                        index_column = get_next_excel_column(index_column)

                    scenario = Scenario(scenario_sheet_name, scenario_type, vehicle_type, years)
                    if scenario_type in self.scenarios.keys():
                        self.scenarios[scenario_type][vehicle_type] = scenario
                    else:
                        self.scenarios[scenario_type] = {
                            vehicle_type: scenario
                        }

            except KeyError:
                continue
