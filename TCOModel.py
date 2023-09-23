from data_objects.Strategy1 import Strategy1
from data_objects.Strategy2 import Strategy2
from data_objects.Strategy3 import Strategy3
from data_objects.Strategy4 import Strategy4
from data_objects.Strategy5 import Strategy5
from data_objects.Vehicle import Vehicle
from excel_interfaces.PANTEIAInterface import PANTEIAInterface
from exceptions import InvalidScenarioSpecified, OutputIsNotSupported
from helpers.GraphHelper import GraphHelper
from Logger import Logger
from datetime import date
import csv

class TCOModel:

    # Model data
    PANTEIA_interface: PANTEIAInterface = None
    fleet: dict = None
    scenarios: dict = None
    output: tuple = None

    # Model constants
    extra_years_after_lifespan: int = None
    increase_factor_after_lifespan: float = None
    transition_margin: float = None
    tax_percentage: float = None
    current_year: int = None,
    final_year: int = None
    valid_scenario_types: tuple = ()
    valid_strategies: dict = {}

    def __init__(self,
                 fleet: dict,
                 scenarios: dict,
                 valid_scenario_names: tuple,
                 output: tuple,
                 extra_years_after_lifespan: int = 3,
                 increase_factor_after_lifespan: float = 2,
                 transition_margin: float = 0.03,
                 tax_percentage: float = 0.25,
                 current_year: int = date.today().year,
                 final_year: int = date.today().year + 10):

        """Initialises a model to calculate TCO.

        :param fleet: The fleet to calculate the TCO for.
        :type fleet: dict
        :param scenarios: The scenarios that should be calculated.
        :type scenarios: dict
        :param valid_scenario_names: All the valid scenario names.
        :type valid_scenario_names: tuple
        :param output: The expected output.
        :type output: tuple
        :param extra_years_after_lifespan: The maximum extra years after the lifespan.
        :type extra_years_after_lifespan: int
        :param increase_factor_after_lifespan: The factor to increase costs after the original lifespan.
        :type increase_factor_after_lifespan: float
        :param transition_margin: The margin for transitioning.
        :type transition_margin: float
        :param tax_percentage: The tax percentage of a company to calculate investment deduction.
        :type tax_percentage: float
        :param current_year: First year of calculation.
        :type current_year: int
        :param final_year: Final year of calculation.
        :type final_year: int


        :return: An instance of TCOModel.
        :rtype: TCOModel
        """

        # Define model parameters
        self.extra_years_after_lifespan = extra_years_after_lifespan
        self.increase_factor_after_lifespan = increase_factor_after_lifespan
        self.transition_margin = transition_margin
        self.tax_percentage = tax_percentage
        self.current_year = current_year
        self.final_year = final_year
        self.output = output

        self.valid_scenario_types = valid_scenario_names
        strategy_1 = Strategy1()
        strategy_2 = Strategy2()
        strategy_3 = Strategy3()
        strategy_4 = Strategy4()
        strategy_5 = Strategy5()
        self.valid_strategies = {
            "strategy_1": strategy_1,
            "strategy_2": strategy_2,
            "strategy_3": strategy_3,
            "strategy_4": strategy_4,
            "strategy_5": strategy_5
        }

        # Initialise excel interface
        self.PANTEIA_interface = PANTEIAInterface()
        self.fleet = fleet
        self.scenarios = scenarios

    def compare_strategies(self, scenario_type: str, strategy_names: tuple = None):

        """Compare a list of strategies against a single scenario.

        :param scenario_type: The specified scenario to use.
        :type scenario_type: str
        :param strategy_names: The names of the strategies to compare.
        :type strategy_names: tuple

        :return: The expected output organised by scenario and strategy.
        :rtype: dict
        """

        # Check if scenario name is valid
        if scenario_type not in self.valid_scenario_types and \
           scenario_type not in self.scenarios.keys():
            raise InvalidScenarioSpecified
        scenario = {
            scenario_type: self.scenarios[scenario_type]
        }

        # Add only valid strategies
        strategies = {}
        if strategy_names is not None:
            strategies = {name: self.valid_strategies[name]
                          for name in strategy_names
                          if name in self.valid_strategies}

        # Default to all strategie
        if len(strategies) < 1:
            strategies = self.valid_strategies

        # Calculate TCO for vehicles in fleet
        fleet_TCO = {number_plate: self.calculate_TCO(vehicle, scenario, strategies)
                     for number_plate, vehicle in self.fleet.items()}

        # Create graphs
        graphs = {}

        # Initialise Graph Helper
        graph_helper = GraphHelper()

        # Create TCO graphs for every vehicle if 10 or less, but skip the first (example).
        if 2 < len(fleet_TCO) < 11:
            vehicle_TCO = {}
            for number_plate in fleet_TCO:

                if number_plate == "voorbeeld":
                    continue

                vehicle_data = fleet_TCO[number_plate]
                vehicle_TCO[number_plate] = graph_helper.plot_vehicle_TCO(number_plate,
                                                                          vehicle_data)
            graphs["vehicle_TCO"] = vehicle_TCO

            # Create charging capacity graphs for every vehicle, but skip the first (example)
            vehicle_charging_capacity = {}
            for number_plate in fleet_TCO:

                if number_plate == "voorbeeld":
                    continue

                vehicle_data = fleet_TCO[number_plate]
                vehicle_charging_capacity[number_plate] = graph_helper.plot_vehicle_charging_capacity(number_plate,
                                                                                                      vehicle_data)
            graphs["vehicle_charging_capacity"] = vehicle_charging_capacity

            vehicle_charging_time = {}
            for number_plate in fleet_TCO:

                if number_plate == "voorbeeld":
                    continue

                vehicle_data = fleet_TCO[number_plate]
                vehicle_charging_time[number_plate] = graph_helper.plot_vehicle_charging_time(number_plate,
                                                                                              vehicle_data)
            graphs["vehicle_charging_time"] = vehicle_charging_time

        # Calculate fleet averages
        fleet_TCO["sum"] = self.calculate_fleet_sum(fleet_TCO)

        # Calculate transition year
        fleet_transition_year = self.calculate_transition_year(fleet_TCO)

        # Create average fleet graphs
        graphs["TCO_total_bar"] = graph_helper.plot_TCO_fleet_averages_bar(fleet_TCO["sum"])
        graphs["TCO_total_cost"] = graph_helper.plot_TCO_fleet_average_cost(fleet_TCO["sum"])
        graphs["TCO_costs_breakdown"] = graph_helper.plot_TCO_costs_breakdown(fleet_TCO["sum"])
        graphs["CO2_total_bar"] = graph_helper.plot_CO2_fleet_averages_bar(fleet_TCO["sum"])
        graphs["CO2_total_emissions"] = graph_helper.plot_TCO_fleet_average_emissions(fleet_TCO["sum"])
        graphs["Capacity_total_bar"] = graph_helper.plot_TCO_fleet_average_charging_capacity(fleet_TCO["sum"])
        graphs["Charging_time_total_bar"] = graph_helper.plot_TCO_fleet_average_charging_time(fleet_TCO["sum"])

        # Add relevant data to data
        data = {
            "fleet_TCO": fleet_TCO,
            "fleet_transition_year": fleet_transition_year,
            "graphs": graphs
        }

        return self.format_data(data)

    def compare_scenarios(self, strategy_name: str, scenario_names: tuple):

        """Compare a list of scenario against a single strategy.

        :param strategy_name: The specified scenario to use.
        :type strategy_name: str
        :param scenario_names: The names of the strategies to compare.
        :type scenario_names: tuple

        :return: The expected output organised by scenario and strategy.
        :rtype: dict
        """

        # Check if scenario name is valid
        if not strategy_name:
            strategy_name = list(self.valid_strategies.keys())[0]
        elif strategy_name not in self.valid_strategies.keys():
            raise InvalidScenarioSpecified
        
        # Get the strategy
        strategy = {
            strategy_name: self.valid_strategies[strategy_name]
        }

        # Add only valid scenarios
        scenarios = {}
        if scenario_names is not None:
            scenarios = {scenario_type: self.valid_scenario_types[scenario_type]
                         for scenario_type in scenario_names
                         if scenario_type in self.valid_scenario_types}

        # Default to all available scenarios
        if len(scenarios) < 1:
            scenarios = self.scenarios

        # Calculate TCO for vehicles in fleet
        fleet_TCO = {number_plate: self.calculate_TCO(vehicle, scenarios, strategy)
                     for number_plate, vehicle in self.fleet.items()}

        # Create graphs dict
        graphs = {}

        # Initialise Graph Helper
        graph_helper = GraphHelper()

        # Create TCO graphs for every vehicle if 10 or less but skip the first (example).
        if 2 < len(fleet_TCO) < 11:
            vehicle_TCO = {}
            for number_plate in list(fleet_TCO.keys()):

                if number_plate == "voorbeeld":
                    continue

                vehicle_data = fleet_TCO[number_plate]
                vehicle_TCO[number_plate] = graph_helper.plot_vehicle_TCO_scenarios(number_plate,
                                                                          vehicle_data)
            graphs["vehicle_TCO"] = vehicle_TCO

            # Create charging capacity graphs for every vehicle
            vehicle_charging_capacity = {}
            for number_plate in fleet_TCO:

                if number_plate == "voorbeeld":
                    continue

                vehicle_data = fleet_TCO[number_plate]
                vehicle_charging_capacity[number_plate] = graph_helper.plot_vehicle_charging_capacity(number_plate,
                                                                                                      vehicle_data)
            graphs["vehicle_charging_capacity"] = vehicle_charging_capacity

            vehicle_charging_time = {}
            for number_plate in fleet_TCO:

                if number_plate == "voorbeeld":
                    continue

                vehicle_data = fleet_TCO[number_plate]
                vehicle_charging_time[number_plate] = graph_helper.plot_vehicle_charging_time(number_plate,
                                                                                              vehicle_data)
            graphs["vehicle_charging_time"] = vehicle_charging_time

        # Calculate fleet total
        fleet_TCO["sum"] = self.calculate_fleet_sum(fleet_TCO)

        # Calculate transition year
        fleet_transition_year = self.calculate_transition_year(fleet_TCO)

        # Create fleet graphs
        graphs["TCO_total_bar"] = graph_helper.plot_TCO_fleet_averages_bar_scenarios(fleet_TCO["sum"])
        graphs["TCO_total_cost"] = graph_helper.plot_TCO_fleet_average_cost_scenarios(fleet_TCO["sum"])
        graphs["TCO_costs_breakdown"] = graph_helper.plot_TCO_costs_breakdown(fleet_TCO["sum"])
        graphs["CO2_total_bar"] = graph_helper.plot_CO2_fleet_averages_bar_scenarios(fleet_TCO["sum"])
        graphs["CO2_total_emissions"] = graph_helper.plot_TCO_fleet_average_emissions_scenarios(fleet_TCO["sum"])
        graphs["Capacity_total_bar"] = graph_helper.plot_TCO_fleet_average_charging_capacity_scenarios(fleet_TCO["sum"])


        # Add relevant data to data
        data = {
            "fleet_TCO": fleet_TCO,
            "fleet_transition_year": fleet_transition_year,
            "graphs": graphs
        }

        return self.format_data(data)

    def format_data(self, data: dict):

        """Format the output data into the expected format.

        :param data: The output data from the model.
        :type data: dict

        :return: The formatted data.
        :rtype: dict
        """

        formatted_data = {}

        # check graphs
        if "graphs" in self.output:
            if "graphs" in data.keys():
                formatted_data["graphs"] = data["graphs"]
            else:
                formatted_data["graphs"] = "Graphs couldn't be found."

        # Check input
        if "input" in self.output:

            formatted_data["original_fleet"] = {number_plate: vehicle.to_dict()
                                                for number_plate, vehicle in self.fleet.items()}
            formatted_data["scenarios"] = {scenario_type: {vehicle_type: year_data.to_dict()
                                                           for vehicle_type, year_data in scenario_data.items()}
                                           for scenario_type, scenario_data in self.scenarios.items()}

        # Check results
        if "results" in self.output:
            if "fleet_TCO" in data.keys():
                formatted_data["results"] = data["fleet_TCO"]
                formatted_data["transition_year"] = data["fleet_transition_year"]
            else:
                formatted_data["results"] = "Results couldn't be found."

        if len(formatted_data.keys()) > 0:
            return formatted_data
        else:
            raise OutputIsNotSupported

    def calculate_TCO(self, vehicle: Vehicle, scenarios: dict, strategies: dict):

        """Calculate the TCO values for a vehicle.

        :param vehicle: The vehicle to calculate the TCO for.
        :type vehicle: Vehicle
        :param scenarios: The scenarios that will be used.
        :type scenarios: dict
        :param strategies: The that will be applied to each scenario.
        :type strategies: dict

        :return: The calculated TCO values organised by scenario and strategy.
        :rtype: dict
        """

        # Iterate over the different scenarios and strategies
        results = {}
        for scenario in scenarios:
            scenario_results = {}
            for strategy in strategies:

                # Reset values
                self.PANTEIA_interface.reset_values()

                # Input vehicle information
                self.PANTEIA_interface.input_vehicle_data(vehicle)

                # Calculate result
                result = strategies[strategy].calculate_TCO(scenarios[scenario][str(vehicle.category+1)],
                                                            vehicle,
                                                            self.PANTEIA_interface,
                                                            self.extra_years_after_lifespan,
                                                            self.increase_factor_after_lifespan,
                                                            self.transition_margin,
                                                            self.tax_percentage,
                                                            self.current_year,
                                                            self.final_year)

                # Reset lifespan values
                self.PANTEIA_interface.reset_technological_lifespan()

                # Append result
                scenario_results[strategy] = result

            # Append scenario results
            results[scenario] = scenario_results

        return results

    def calculate_fleet_sum(self, fleet_TCO: dict):

        """Calculates the total TCO value for a fleet.

        :param fleet_TCO: The fleet data to get the sum from.
        :type fleet_TCO: dict

        :return: The average TCO values
        :rtype: dict
        """

        amount_of_vehicles = len(fleet_TCO)
        sums = {}

        # Get the sum for all the values
        for number_plate, scenarios in fleet_TCO.items():

            if number_plate == "voorbeeld":
                continue

            for scenario, strategies in scenarios.items():

                if scenario not in sums:
                    sums[scenario] = {}

                for strategy, years in strategies.items():

                    if strategy not in sums[scenario]:
                        sums[scenario][strategy] = {}

                    for year, year_data in years.items():

                        if year not in sums[scenario][strategy]:
                            sums[scenario][strategy][year] = {}

                        for prop, value in year_data.items():

                            try:
                                sums[scenario][strategy][year][prop] = sums[scenario][strategy][year][prop] + value
                            except:
                                sums[scenario][strategy][year][prop] = value

        # # Get the average
        # averages = {scenario: {strategy: {year: {prop: value/amount_of_vehicles
        #                                          for prop, value in props.items()}
        #                                   for year, props in years.items()}
        #                        for strategy, years in strategies.items()}
        #             for scenario, strategies in sums.items()}

        return sums

    def calculate_transition_year(self, fleet_TCO: dict):

        """Calculates the transition year for each vehicle

        :param fleet_TCO: The fleet data to get the transition year from.
        :type fleet_TCO: dict

        :return: The transition year of each vehicle
        :rtype: dict
        """

        transition_year = {}

        # Get the sum for all the values
        for number_plate, scenarios in fleet_TCO.items():

            if number_plate == "sum" or number_plate == "voorbeeld":
                continue
            if number_plate not in transition_year:
                transition_year[number_plate] = {}
            for scenario, strategies in scenarios.items():
                if scenario not in transition_year[number_plate]:
                    transition_year[number_plate][scenario] = {}
                for strategy, years in strategies.items():
                    for year, year_data in years.items():
                        if year_data['transition_year'] != 0:
                            transition_year[number_plate][scenario][strategy] = year
                            break
                        else:
                            transition_year[number_plate][scenario][strategy] = ">" + str(self.final_year - 1)

        return transition_year

