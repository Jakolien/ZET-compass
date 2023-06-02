from data_objects.AbstractStrategy import AbstractStrategy
from data_objects.Scenario import Scenario
from data_objects.Vehicle import Vehicle
from excel_interfaces.PANTEIAInterface import PANTEIAInterface
from Logger import Logger
import itertools

class Strategy1(AbstractStrategy):

    def __int__(self):

        self.name = "Strategy 1"

    def calculate_TCO(self,
                      scenario: Scenario,
                      vehicle: Vehicle,
                      PANTEIA_interface: PANTEIAInterface,
                      extra_years_after_lifespan: int,
                      increase_factor_after_lifespan: float,
                      transition_margin: float,
                      tax_percentage: float,
                      current_year: int,
                      final_year: int,
                      logger: Logger):

        """Calculates the TCO values according to the following logic:
        Switch to a new electric vehicle, if the current vehicle is written off and it's technologically possible.
        Don't buy new diesel vehicles.

        :param scenario: The scenario that will be used in the calculations.
        :type scenario: Scenario
        :param vehicle: The vehicle that will be used in the calculations.
        :type vehicle: Vehicle
        :param PANTEIA_interface: The interface to the PANTEIA model.
        :type PANTEIA_interface: PANTEIAInterface
        :param charging_time_depot: The amount of hours to charge on the depot.
        :type charging_time_depot: int
        :param charging_time_public: The amount of hours to charge in public.
        :type charging_time_public: int
        :param extra_years_after_lifespan: The extra years after the lifespan a vehicle should be kept.
        :type: int
        :param increase_factor_after_lifespan: The factor to increase maintenance costs after the vehicle's lifespan.
        :type increase_factor_after_lifespan: float
        :param transition_margin: The relative percentage to determine the transition threshold.
        :type transition_margin: float
        :param tax_percentage: The tax percentage of a company.
        :type tax_percentage: float
        :param current_year: First year of calculation.
        :type current_year: int
        :param final_year: Final year of calculation.
        :type final_year: int

        :return: The calculated TCO values for the given vehicle and scenario.
        :rtype: dict
        """

        # Get vehicle age
        original_vehicle_age = vehicle.get_current_age("Europe/Amsterdam")

        # Get technological lifespan
        lifespans = PANTEIA_interface.get_technological_lifespan()
        electric_lifespan = lifespans.get("electric")
        diesel_lifespan = lifespans.get("diesel")

        # Get scenario year data
        years = scenario.years

        # set the number of years to compute
        years_slice = dict(itertools.islice(years.items(), 10))

        results = {}
        current_vehicle_age = original_vehicle_age
        current_fuel_type = vehicle.fuel_type
        current_vehicle_index = vehicle.category
        charging_time_depot = vehicle.charging_time_depot
        charging_time_public = vehicle.charging_time_public
        current_lifespan = diesel_lifespan if current_fuel_type.lower() == "diesel" else electric_lifespan #TODO change to list of fuel types, also for other strategies
        list_of_fuel_types = ["Diesel","CNG","Blauwe diesel","Benzine","LNG"]

        # Update fixed parameters
        PANTEIA_interface.update_fixed_parameters(current_lifespan,
                                                  current_vehicle_index,
                                                  charging_time_depot,
                                                  charging_time_public,
                                                  tax_percentage,
                                                  years[current_year],
                                                  years[current_year + current_lifespan])

        # Update variable parameters for current year
        PANTEIA_interface.update_variable_parameters(years[current_year])

        # Input vehicle information
        PANTEIA_interface.input_vehicle_data(vehicle)

        # iterate over years
        for year in years_slice:

            # Get scenario data each year
            year_data = years[year]

            # Update variable parameters each year
            PANTEIA_interface.update_variable_parameters(year_data)

            # Check if optimal mix is valid
            is_optimal_mix_valid = PANTEIA_interface.is_optimal_mix_valid()

            # Determine if vehicle needs to be changed
            if current_vehicle_age >= current_lifespan:
                # If currently diesel, switch to electric
                if current_fuel_type.capitalize() in list_of_fuel_types and \
                   is_optimal_mix_valid:
                    current_fuel_type = "Elektrisch"
                    current_lifespan = electric_lifespan
                    current_vehicle_age = 0

                    # Update fixed parameters
                    PANTEIA_interface.update_fixed_parameters(current_lifespan,
                                                              current_vehicle_index,
                                                              charging_time_depot,
                                                              charging_time_public,
                                                              tax_percentage,
                                                              year_data,
                                                              years[year + current_lifespan])

                # If currently electric, buy new electric vehicle
                if current_fuel_type.capitalize() == "Elektrisch":
                    # Reset vehicle age
                    current_vehicle_age = 0

                    # Update fixed parameters
                    PANTEIA_interface.update_fixed_parameters(current_lifespan,
                                                              current_vehicle_index,
                                                              charging_time_depot,
                                                              charging_time_public,
                                                              tax_percentage,
                                                              year_data,
                                                              years[year + current_lifespan])

            # Check if vehicle is past lifespan
            if current_vehicle_age > current_lifespan:
                self.increase_maintenance_costs(current_fuel_type,
                                                current_vehicle_age,
                                                current_lifespan,
                                                increase_factor_after_lifespan,
                                                PANTEIA_interface)

                # decrease yearly depreciation costs, because vehicle is already paid off
                PANTEIA_interface.decrease_yearly_depreciation_costs(current_fuel_type, current_vehicle_age)
            else:
                PANTEIA_interface.reset_yearly_depreciation_costs()

            # Check costs for Zero Emission zones
            if current_fuel_type.capitalize() == "Diesel" and \
                    vehicle.drives_in_future_ZE_zone and \
               not self.is_allowed_in_ZE_zone(vehicle, current_vehicle_age, int(year)):
                PANTEIA_interface.set_ZE_costs(year_data)
                pass
            else:
                PANTEIA_interface.reset_ZE_costs()
                pass

            # Check if exclusive charging at depot is possible
            is_exclusive_charging_at_depot_possible = PANTEIA_interface.is_exclusive_home_loading_valid()

            # workaround until bug solved
            is_exclusive_charging_at_depot_possible = False

            # Calculate TCO
            result = self.get_results(current_fuel_type,
                                      is_exclusive_charging_at_depot_possible,
                                      PANTEIA_interface)

            # Append year results
            results[year] = result

            # Increment age
            current_vehicle_age += 1

        return results
