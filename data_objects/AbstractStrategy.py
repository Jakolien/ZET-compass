from abc import abstractmethod
from data_objects.Scenario import Scenario
from data_objects.Vehicle import Vehicle
from excel_interfaces.PANTEIAInterface import PANTEIAInterface
from Logger import Logger
import itertools

class AbstractStrategy:

    name: str = None

    @abstractmethod
    def calculate_TCO(self,
                      scenario: Scenario,
                      vehicle: Vehicle,
                      PANTEIA_interface: PANTEIAInterface,
                      extra_years_after_lifespan: int,
                      increase_factor_after_lifespan: float,
                      transition_margin: float):

        """Calculates the TCO values according to the following logic:
        {Strategy description here}

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

        :return: The calculated TCO values for the given vehicle and scenario.
        :rtype: dict
        """

        pass

    def is_allowed_in_ZE_zone(self, vehicle: Vehicle, current_age: int, year: int):

        """Determines whether the vehicle is allowed to be in a Zero Emission zone.

        :param vehicle: The vehicle.
        :type vehicle: Vehicle
        :param current_age: The current age of the vehicle in years.
        :type current_age: int
        :param year: The year to determine for.
        :type year: int

        :return: Whether the vehicle is allowed to be in a ZE zone.
        :rtype: bool
        """

        is_allowed = True

        # No measures yet
        if year < 2025:
            is_allowed = True

        # Measures for all diesel vehicles
        elif year > 2029:
            is_allowed = False

        # Transitional period
        else:
            age_in_2025 = current_age - (year - 2025)

            # If less than 1 year, then automatically banned
            if age_in_2025 < 1:
                is_allowed = False
            else:

                # For N1 types
                if vehicle.type in ('Kleine bestelwagen', 'Middel bestelwagen', 'Middel bestelwagen luxe',
                                    'Grote bestelwagen') and \
                   year <= 2026 and \
                   vehicle.euronorm > 4:
                    is_allowed = True
                elif vehicle.type in ('Kleine bestelwagen', 'Middel bestelwagen', 'Middel bestelwagen luxe',
                                      'Grote bestelwagen') and \
                     year <= 2027 and \
                     vehicle.euronorm > 5:
                    is_allowed = True
                else:
                    is_allowed = False

                # For N2 types
                if vehicle.type in ("Kleine bakwagen (12t)", "Grote bakwagen (18t)") and \
                   age_in_2025 <= 5:
                    is_allowed = True
                elif vehicle.type in ("Kleine bakwagen (12t)", "Grote bakwagen (18t)"):
                    is_allowed = False

                # For N3 types
                if vehicle.type in ('Trekker-oplegger',) and \
                   age_in_2025 <= 8:
                    is_allowed = True
                elif vehicle.type in ('Trekker-oplegger',):
                    is_allowed = False

        return is_allowed

    def increase_maintenance_costs(self,
                                   current_fuel_type: str,
                                   current_vehicle_age: int,
                                   current_lifespan: int,
                                   increase_factor_after_lifespan: float,
                                   PANTEIA_interface: PANTEIAInterface):

        """Calculates and increases the maintenance cost.

        :param current_fuel_type: The vehicles current fuel type.
        :type current_fuel_type: str
        :param current_vehicle_age: The current age of the vehicle.
        :type current_vehicle_age: int
        :param current_lifespan: The current lifespan of the vehicle.
        :type current_lifespan: int
        :param increase_factor_after_lifespan: The yearly factor to increase the lifespan by.
        :type increase_factor_after_lifespan: float
        :param PANTEIA_interface: The PANTEIA interface to update.
        :type PANTEIA_interface: PANTEIAInterface

        :return: Nothing
        :rtype: None
        """

        # Increase maintenance costs
        years_past_lifespan = current_vehicle_age - current_lifespan
        # If current_vehicle_age = 8 and current_lifespan = 7,
        # Then the increased maintenance factor is calculated with an exponent of 2,
        # While it is only 1 year after the lifespan
        increased_maintenance_factor = pow(increase_factor_after_lifespan, years_past_lifespan)
        PANTEIA_interface.increase_maintenance_factor(current_fuel_type, increased_maintenance_factor)

    def transition_year_reached(self, margin: float, PANTEIA_interface: PANTEIAInterface):

        """Determine whether the transition year has been reached.

        :param margin: The relative percentage to determine the transition threshold.
        :type margin: float
        :param PANTEIA_interface: The PANTEIA interface to use.
        :type PANTEIA_interface: PANTEIAInterface

        :return: Whether the transition year has been reached.
        :rtype: bool
        """

        # Assume diesel is cheaper
        is_transition_year_reached = False

        is_scenario_valid = PANTEIA_interface.is_optimal_mix_valid()
        is_depot_loading_possible = PANTEIA_interface.is_exclusive_home_loading_valid()
        total_TCO_cost_depot_charging = PANTEIA_interface.get_total_TCO_cost_depot_charging()
        total_TCO_cost_optimal_mix = PANTEIA_interface.get_total_TCO_cost_optimal_mix()
        total_TCO_cost_diesel = PANTEIA_interface.get_total_TCO_cost_diesel()

        # Calculations
        transition_threshold = margin * int(total_TCO_cost_diesel)

        is_depot_charging_cheaper_than_diesel = False
        if total_TCO_cost_depot_charging and total_TCO_cost_diesel:
            is_depot_charging_cheaper_than_diesel = \
                (total_TCO_cost_depot_charging - total_TCO_cost_diesel) < transition_threshold

        is_optimal_mix_cheaper_than_diesel = False
        if total_TCO_cost_optimal_mix and total_TCO_cost_diesel:
            is_optimal_mix_cheaper_than_diesel = \
                (total_TCO_cost_optimal_mix - total_TCO_cost_diesel) < transition_threshold

        # If scenario is not valid, then not currently possible
        if not is_scenario_valid:
            is_transition_year_reached = False

        # Check if charging at depot is cheaper than diesel
        elif is_depot_loading_possible and is_depot_charging_cheaper_than_diesel:
            is_transition_year_reached = True

        # Check if optimal is cheaper than diesel
        elif not is_depot_loading_possible and is_optimal_mix_cheaper_than_diesel:
            is_transition_year_reached = True

        return is_transition_year_reached

    def get_results(self,
                    current_fuel_type: str,
                    is_exclusive_charging_at_depot_possible: bool,
                    PANTEIA_interface: PANTEIAInterface):

        """Get the TCO model results.

        :param current_fuel_type: The vehicles current fuel type.
        :type current_fuel_type: str
        :param is_exclusive_charging_at_depot_possible: Whether exclusive charging at depot is possible.
        :type is_exclusive_charging_at_depot_possible: bool
        :param PANTEIA_interface: The PANTEIA interface to use.
        :type PANTEIA_interface: PANTEIAInterface

        :return: The TCO model results.
        :rtype: dict
        """

        list_of_fuel_types = ["Diesel", "CNG", "Blauwe diesel", "Benzine", "LNG"]

        if current_fuel_type.capitalize() in list_of_fuel_types:
            result = PANTEIA_interface.get_TCO_diesel()
        else:
            result = PANTEIA_interface.get_TCO_electric(is_exclusive_charging_at_depot_possible)

        return result
