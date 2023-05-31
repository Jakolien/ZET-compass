def from_dict(data: dict):

    """Construct a scenario year from a dictionary.

    :param data: The input data.
    :type data: dict

    :return: The constructed scenario.
    :rtype: ScenarioYear
    """

    scenario_year = ScenarioYear(data["year"],
                                 data["diesel_price_in_euro"],
                                 data["electric_price_in_euro"],
                                 data["capacity_in_kWh"],
                                 data["repair_costs_EV_euro_per_year"],
                                 data["maintenance_costs_EV_euro_per_km"],
                                 data["maintenance_costs_diesel_euro_per_km"],
                                 data["standstil_EV_in_days"],
                                 data["subsidies_EV_in_euro"],
                                 data["CO2_price_in_euro_per_ton"],
                                 data["efficiency_diesel_in_liter_per_km"],
                                 data["efficiency_electricity_in_kWh_per_km"],
                                 data["electricity_price_private_excluding_tax_in_euro_per_kWh"],
                                 data["electricity_price_public_excluding_tax_in_euro_per_kWh"],
                                 data["gross_purchase_cost_charging_system_in_euro"],
                                 data["gross_installation_cost_charging_system_in_euro"],
                                 data["fuel_price_diesel_excluding_tax_in_euro_per_liter"],
                                 data["change_in_excise_duty_diesel_in_percentage"],
                                 data["vehicle_tax_diesel_in_euro_per_year"],
                                 data["vehicle_tax_electric_in_euro_per_year"],
                                 data["MIA_in_euro_per_lifespan"],
                                 data["VAMIL_in_euro_per_lifespan"],
                                 data["energy_subsidy_in_euro_per_kWh"],
                                 data["fixed_ZE_vehicle_tax_in_euro_per_year"],
                                 data["difference_truck_toll_tax_in_euro_per_km"],
                                 data["subsidy_charging_system_installation_in_euro_per_installation"],
                                 data["residual_value_EV_year_1_in_percentage"],
                                 data["residual_value_EV_year_2_in_percentage"],
                                 data["residual_value_EV_year_3_in_percentage"],
                                 data["residual_value_EV_year_4_in_percentage"],
                                 data["residual_value_EV_year_5_in_percentage"],
                                 data["residual_value_EV_year_6_in_percentage"],
                                 data["residual_value_EV_year_7_in_percentage"],
                                 data["residual_value_EV_year_8_in_percentage"],
                                 data["residual_value_EV_year_9_in_percentage"],
                                 data["residual_value_EV_year_10_in_percentage"],
                                 data["residual_value_EV_year_11_in_percentage"],
                                 data["residual_value_EV_year_12_in_percentage"],
                                 data["residual_value_EV_year_13_in_percentage"],
                                 data["residual_value_EV_year_14_in_percentage"],
                                 data["residual_value_EV_year_15_in_percentage"],
                                 data["residual_value_diesel_year_1_in_percentage"],
                                 data["residual_value_diesel_year_2_in_percentage"],
                                 data["residual_value_diesel_year_3_in_percentage"],
                                 data["residual_value_diesel_year_4_in_percentage"],
                                 data["residual_value_diesel_year_5_in_percentage"],
                                 data["residual_value_diesel_year_6_in_percentage"],
                                 data["residual_value_diesel_year_7_in_percentage"],
                                 data["residual_value_diesel_year_8_in_percentage"],
                                 data["residual_value_diesel_year_9_in_percentage"],
                                 data["residual_value_diesel_year_10_in_percentage"],
                                 data["residual_value_diesel_year_11_in_percentage"],
                                 data["residual_value_diesel_year_12_in_percentage"],
                                 data["residual_value_diesel_year_13_in_percentage"],
                                 data["residual_value_diesel_year_14_in_percentage"],
                                 data["residual_value_diesel_year_15_in_percentage"],
                                 data["charging_capacity_external_charging_pole"],
                                 data["charging_capacity_charging_pole_on_depot"],
                                 data["needed_charging_capacity_depot"],
                                 data["needed_charging_capacity_in_transit"],
                                 data["AC37_at_home"],
                                 data["AC10_in_transit"],
                                 data["AC20_in_transit"],
                                 data["AC20_at_home"],
                                 data["FC50_in_transit"],
                                 data["FC50_at_home"],
                                 data["HPC150_in_transit"],
                                 data["HPC150_at_home"],
                                 data["HPC350_in_transit"],
                                 data["HPC350_at_home"])

    return scenario_year


class ScenarioYear:

    year: str = None
    diesel_price_in_euro: float = None
    electric_price_in_euro: float = None
    capacity_in_kWh: int = None
    repair_costs_EV_euro_per_year: float = None
    maintenance_costs_EV_euro_per_km: float = None
    maintenance_costs_diesel_euro_per_km: float = None
    standstil_EV_in_days: float = None
    subsidies_EV_in_euro: float = None
    CO2_price_in_euro_per_ton: float = None
    efficiency_diesel_in_liter_per_km: float = None
    efficiency_electricity_in_kWh_per_km: float = None
    electricity_price_private_excluding_tax_in_euro_per_kWh: float = None
    electricity_price_public_excluding_tax_in_euro_per_kWh: float = None
    gross_purchase_cost_charging_system_in_euro: float = None
    gross_installation_cost_charging_system_in_euro: float = None
    fuel_price_diesel_excluding_tax_in_euro_per_liter: float = None
    change_in_excise_duty_diesel_in_percentage: float = None
    vehicle_tax_diesel_in_euro_per_year: float = None
    vehicle_tax_electric_in_euro_per_year: float = None
    MIA_in_euro_per_lifespan: float = None
    VAMIL_in_euro_per_lifespan: float = None
    energy_subsidy_in_euro_per_kWh: float = None
    fixed_ZE_vehicle_tax_in_euro_per_year: float = None
    difference_truck_toll_tax_in_euro_per_km: float = None
    subsidy_charging_system_installation_in_euro_per_installation: float = None
    residual_value_EV_year_1_in_percentage: float = None
    residual_value_EV_year_2_in_percentage: float = None
    residual_value_EV_year_3_in_percentage: float = None
    residual_value_EV_year_4_in_percentage: float = None
    residual_value_EV_year_5_in_percentage: float = None
    residual_value_EV_year_6_in_percentage: float = None
    residual_value_EV_year_7_in_percentage: float = None
    residual_value_EV_year_8_in_percentage: float = None
    residual_value_EV_year_9_in_percentage: float = None
    residual_value_EV_year_10_in_percentage: float = None
    residual_value_EV_year_11_in_percentage: float = None
    residual_value_EV_year_12_in_percentage: float = None
    residual_value_EV_year_13_in_percentage: float = None
    residual_value_EV_year_14_in_percentage: float = None
    residual_value_EV_year_15_in_percentage: float = None
    residual_value_diesel_year_1_in_percentage: float = None
    residual_value_diesel_year_2_in_percentage: float = None
    residual_value_diesel_year_3_in_percentage: float = None
    residual_value_diesel_year_4_in_percentage: float = None
    residual_value_diesel_year_5_in_percentage: float = None
    residual_value_diesel_year_6_in_percentage: float = None
    residual_value_diesel_year_7_in_percentage: float = None
    residual_value_diesel_year_8_in_percentage: float = None
    residual_value_diesel_year_9_in_percentage: float = None
    residual_value_diesel_year_10_in_percentage: float = None
    residual_value_diesel_year_11_in_percentage: float = None
    residual_value_diesel_year_12_in_percentage: float = None
    residual_value_diesel_year_13_in_percentage: float = None
    residual_value_diesel_year_14_in_percentage: float = None
    residual_value_diesel_year_15_in_percentage: float = None
    charging_capacity_external_charging_pole: float = None
    charging_capacity_charging_pole_on_depot: float = None
    needed_charging_capacity_depot: float = None
    needed_charging_capacity_in_transit: float = None
    AC37_at_home: float = None
    AC10_in_transit: float = None
    AC20_in_transit: float = None
    AC20_at_home: float = None
    FC50_in_transit: float = None
    FC50_at_home: float = None
    HPC150_in_transit: float = None
    HPC150_at_home: float = None
    HPC350_in_transit: float = None
    HPC350_at_home: float = None

    def __init__(self,
                 year: int,
                 diesel_price_in_euro: float,
                 electric_price_in_euro: float,
                 capacity_in_kWh: int,
                 repair_costs_EV_euro_per_year: float,
                 maintenance_costs_EV_euro_per_km: float,
                 maintenance_costs_diesel_euro_per_km: float,
                 standstil_EV_in_days: float,
                 subsidies_EV_in_euro: float,
                 CO2_price_in_euro_per_ton: float,
                 efficiency_diesel_in_liter_per_km: float,
                 efficiency_electricity_in_kWh_per_km: float,
                 electricity_price_private_excluding_tax_in_euro_per_kWh: float,
                 electricity_price_public_excluding_tax_in_euro_per_kWh: float,
                 gross_purchase_cost_charging_system_in_euro: float,
                 gross_installation_cost_charging_system_in_euro: float,
                 fuel_price_diesel_excluding_tax_in_euro_per_liter: float,
                 change_in_excise_duty_diesel_in_percentage: float,
                 vehicle_tax_diesel_in_euro_per_year: float,
                 vehicle_tax_electric_in_euro_per_year: float,
                 MIA_in_euro_per_lifespan: float,
                 VAMIL_in_euro_per_lifespan: float,
                 energy_subsidy_in_euro_per_kWh: float,
                 fixed_ZE_vehicle_tax_in_euro_per_year: float,
                 difference_truck_toll_tax_in_euro_per_km: float,
                 subsidy_charging_system_installation_in_euro_per_installation: float,
                 residual_value_EV_year_1_in_percentage: float,
                 residual_value_EV_year_2_in_percentage: float,
                 residual_value_EV_year_3_in_percentage: float,
                 residual_value_EV_year_4_in_percentage: float,
                 residual_value_EV_year_5_in_percentage: float,
                 residual_value_EV_year_6_in_percentage: float,
                 residual_value_EV_year_7_in_percentage: float,
                 residual_value_EV_year_8_in_percentage: float,
                 residual_value_EV_year_9_in_percentage: float,
                 residual_value_EV_year_10_in_percentage: float,
                 residual_value_EV_year_11_in_percentage: float,
                 residual_value_EV_year_12_in_percentage: float,
                 residual_value_EV_year_13_in_percentage: float,
                 residual_value_EV_year_14_in_percentage: float,
                 residual_value_EV_year_15_in_percentage: float,
                 residual_value_diesel_year_1_in_percentage: float,
                 residual_value_diesel_year_2_in_percentage: float,
                 residual_value_diesel_year_3_in_percentage: float,
                 residual_value_diesel_year_4_in_percentage: float,
                 residual_value_diesel_year_5_in_percentage: float,
                 residual_value_diesel_year_6_in_percentage: float,
                 residual_value_diesel_year_7_in_percentage: float,
                 residual_value_diesel_year_8_in_percentage: float,
                 residual_value_diesel_year_9_in_percentage: float,
                 residual_value_diesel_year_10_in_percentage: float,
                 residual_value_diesel_year_11_in_percentage: float,
                 residual_value_diesel_year_12_in_percentage: float,
                 residual_value_diesel_year_13_in_percentage: float,
                 residual_value_diesel_year_14_in_percentage: float,
                 residual_value_diesel_year_15_in_percentage: float,
                 charging_capacity_external_charging_pole: float,
                 charging_capacity_charging_pole_on_depot: float,
                 needed_charging_capacity_depot: float,
                 needed_charging_capacity_in_transit: float,
                 AC37_at_home: float,
                 AC10_in_transit: float,
                 AC20_in_transit: float,
                 AC20_at_home: float,
                 FC50_in_transit: float,
                 FC50_at_home: float,
                 HPC150_in_transit: float,
                 HPC150_at_home: float,
                 HPC350_in_transit: float,
                 HPC350_at_home: float):

        """Initialises a scenario year data object.

        :param year: The year that the data belongs to.
        :type year: int
        :param diesel_price_in_euro: The price for a diesel vehicle in euro.
        :type diesel_price_in_euro: float
        :param electric_price_in_euro: The price for an electric vehicle in euro.
        :type electric_price_in_euro: float
        :param capacity_in_kWh: The current electric capacity in kWh.
        :type capacity_in_kWh: int
        :param repair_costs_EV_euro_per_year: The yearly repair costs for an electric vehicle.
        :type repair_costs_EV_euro_per_year: float
        :param maintenance_costs_EV_euro_per_km: The yearly maintenance costs for an electric vehicle.
        :type maintenance_costs_EV_euro_per_km: float
        :param maintenance_costs_diesel_euro_per_km: The yearly maintenance costs for a diesel vehicle.
        :type maintenance_costs_diesel_euro_per_km: float
        :param standstil_EV_in_days: The yearly amount of time spent on maintenance and repairs in days.
        :type standstil_EV_in_days: float
        :param subsidies_EV_in_euro: The yearly amount of subsidies for electric vehicles.
        :type subsidies_EV_in_euro: float
        :param CO2_price_in_euro_per_ton: The amount of fines for CO2 emissions in euro per ton.
        :type CO2_price_in_euro_per_ton: float
        :param efficiency_diesel_in_liter_per_km: The fuel efficiency of diesel in liters per km.
        :type efficiency_diesel_in_liter_per_km: float
        :param efficiency_electricity_in_kWh_per_km: The fuel efficiency of electricity in kWh per km.
        :type efficiency_electricity_in_kWh_per_km: float
        :param electricity_price_private_excluding_tax_in_euro_per_kWh: The price of electricity on depot in euro per
        kWh (without taxes).
        :type electricity_price_private_excluding_tax_in_euro_per_kWh: float
        :param electricity_price_public_excluding_tax_in_euro_per_kWh: The price of electricity in public loading
        facilities in euro per kWh (without taxes).
        :type electricity_price_public_excluding_tax_in_euro_per_kWh: float
        :param gross_purchase_cost_charging_system_in_euro: The cost of an electric charging system in euro
            (with taxes).
        :type gross_purchase_cost_charging_system_in_euro: float
        :param gross_installation_cost_charging_system_in_euro: The cost of installing an electric charging system
            in euro (with taxes).
        :type gross_installation_cost_charging_system_in_euro: float
        :param fuel_price_diesel_excluding_tax_in_euro_per_liter: The price of diesel in euro per liter (without taxes).
        :type fuel_price_diesel_excluding_tax_in_euro_per_liter: float
        :param change_in_excise_duty_diesel_in_percentage: The relative change in diesel excise duty in percentages.
        :type change_in_excise_duty_diesel_in_percentage: float
        :param vehicle_tax_diesel_in_euro_per_year: The yearly vehicle (road) tax for diesel vehicles in euro.
        :type vehicle_tax_diesel_in_euro_per_year: float
        :param vehicle_tax_electric_in_euro_per_year: The yearly vehicle (road) tax for electric vehicles in euro.
        :type vehicle_tax_electric_in_euro_per_year: float
        :param MIA_in_euro_per_lifespan: Investment deduction for electric vehicles and loading infrastructure
        :type MIA_in_euro_per_lifespan: float
        :param VAMIL_in_euro_per_lifespan: Investment deduction for electric N2 and N3 vehicles and loading infrastructure.
        :type VAMIL_in_euro_per_lifespan: float
        :param energy_subsidy_in_euro_per_kWh: The energy subsidy provided for electric vehicles in euro per kWh.
        :type energy_subsidy_in_euro_per_kWh: float
        :param fixed_ZE_vehicle_tax_in_euro_per_year: The yearly vehicle tax/fine for vehicles
            that operate within Zero Emission zones, but still use fossil fuels.
        :type fixed_ZE_vehicle_tax_in_euro_per_year: float
        :param difference_truck_toll_tax_in_euro_per_km: The difference in toll taxes for trucks in euro per km.
        :type difference_truck_toll_tax_in_euro_per_km: float
        :param subsidy_charging_system_installation_in_euro_per_installation:
        :type subsidy_charging_system_installation_in_euro_per_installation: float
        :param residual_value_EV_year_1_in_percentage: The residual value of a 1 year old electric vehicle.
        :type residual_value_EV_year_1_in_percentage: float
        :param residual_value_EV_year_2_in_percentage: The residual value of a 2 year old electric vehicle.
        :type residual_value_EV_year_2_in_percentage: float
        :param residual_value_EV_year_3_in_percentage: The residual value of a 3 year old electric vehicle.
        :type residual_value_EV_year_3_in_percentage: float
        :param residual_value_EV_year_4_in_percentage: The residual value of a 4 year old electric vehicle.
        :type residual_value_EV_year_4_in_percentage: float
        :param residual_value_EV_year_5_in_percentage: The residual value of a 5 year old electric vehicle.
        :type residual_value_EV_year_5_in_percentage: float
        :param residual_value_EV_year_6_in_percentage: The residual value of a 6 year old electric vehicle.
        :type residual_value_EV_year_6_in_percentage: float
        :param residual_value_EV_year_7_in_percentage: The residual value of a 7 year old electric vehicle.
        :type residual_value_EV_year_7_in_percentage: float
        :param residual_value_EV_year_8_in_percentage: The residual value of a 8 year old electric vehicle.
        :type residual_value_EV_year_8_in_percentage: float
        :param residual_value_EV_year_9_in_percentage: The residual value of a 9 year old electric vehicle.
        :type residual_value_EV_year_9_in_percentage: float
        :param residual_value_EV_year_10_in_percentage: The residual value of a 10 year old electric vehicle.
        :type residual_value_EV_year_10_in_percentage: float
        :param residual_value_EV_year_11_in_percentage: The residual value of a 11 year old electric vehicle.
        :type residual_value_EV_year_11_in_percentage: float
        :param residual_value_EV_year_12_in_percentage: The residual value of a 12 year old electric vehicle.
        :type residual_value_EV_year_12_in_percentage: float
        :param residual_value_EV_year_13_in_percentage: The residual value of a 13 year old electric vehicle.
        :type residual_value_EV_year_13_in_percentage: float
        :param residual_value_EV_year_14_in_percentage: The residual value of a 14 year old electric vehicle.
        :type residual_value_EV_year_14_in_percentage: float
        :param residual_value_EV_year_15_in_percentage: The residual value of a 15 year old electric vehicle.
        :type residual_value_EV_year_15_in_percentage: float
        :param residual_value_diesel_year_1_in_percentage: The residual value of a 1 year old diesel vehicle.
        :type residual_value_diesel_year_1_in_percentage: float
        :param residual_value_diesel_year_2_in_percentage: The residual value of a 2 year old diesel vehicle.
        :type residual_value_diesel_year_2_in_percentage: float
        :param residual_value_diesel_year_3_in_percentage: The residual value of a 3 year old diesel vehicle.
        :type residual_value_diesel_year_3_in_percentage: float
        :param residual_value_diesel_year_4_in_percentage: The residual value of a 4 year old diesel vehicle.
        :type residual_value_diesel_year_4_in_percentage: float
        :param residual_value_diesel_year_5_in_percentage: The residual value of a 5 year old diesel vehicle.
        :type residual_value_diesel_year_5_in_percentage: float
        :param residual_value_diesel_year_6_in_percentage: The residual value of a 6 year old diesel vehicle.
        :type residual_value_diesel_year_6_in_percentage: float
        :param residual_value_diesel_year_7_in_percentage: The residual value of a 7 year old diesel vehicle.
        :type residual_value_diesel_year_7_in_percentage: float
        :param residual_value_diesel_year_8_in_percentage: The residual value of a 8 year old diesel vehicle.
        :type residual_value_diesel_year_8_in_percentage: float
        :param residual_value_diesel_year_9_in_percentage: The residual value of a 9 year old diesel vehicle.
        :type residual_value_diesel_year_9_in_percentage: float
        :param residual_value_diesel_year_10_in_percentage: The residual value of a 10 year old diesel vehicle.
        :type residual_value_diesel_year_10_in_percentage: float
        :param residual_value_diesel_year_11_in_percentage: The residual value of a 11 year old diesel vehicle.
        :type residual_value_diesel_year_11_in_percentage: float
        :param residual_value_diesel_year_12_in_percentage: The residual value of a 12 year old diesel vehicle.
        :type residual_value_diesel_year_12_in_percentage: float
        :param residual_value_diesel_year_13_in_percentage: The residual value of a 13 year old diesel vehicle.
        :type residual_value_diesel_year_13_in_percentage: float
        :param residual_value_diesel_year_14_in_percentage: The residual value of a 14 year old diesel vehicle.
        :type residual_value_diesel_year_14_in_percentage: float
        :param residual_value_diesel_year_15_in_percentage: The residual value of a 15 year old diesel vehicle.
        :type residual_value_diesel_year_15_in_percentage: float
        :param charging_capacity_external_charging_pole: The charging capacity of an external (public) charging pole.
        :type charging_capacity_external_charging_pole: float
        :param charging_capacity_charging_pole_on_depot: The charging capacity of a charging pole on depot.
        :type charging_capacity_charging_pole_on_depot: float
        :param needed_charging_capacity_depot: The charging capacity necessary for charging on depot.
        :type needed_charging_capacity_depot: float
        :param needed_charging_capacity_in_transit: The charging capacity necessary for charging in transit.
        :type needed_charging_capacity_in_transit: float
        :param AC37_at_home: The charging cost of a AC3.7 charging pole (at home) per kWh in euro.
        :type AC37_at_home: float
        :param AC10_in_transit: The charging cost of a AC10 charging pole (in transit) per kWh in euro.
        :type AC10_in_transit: float
        :param AC20_in_transit: The charging cost of a AC20 charging pole (in transit) per kWh in euro.
        :type AC20_in_transit: float
        :param AC20_at_home: The charging cost of a AC20 charging pole (at home) per kWh in euro.
        :type AC20_at_home: float
        :param FC50_in_transit: The charging cost of a FC50 charging pole (in transit) per kWh in euro.
        :type FC50_in_transit: float
        :param FC50_at_home: The charging cost of a FC50 charging pole (at home) per kWh in euro.
        :type FC50_at_home: float
        :param HPC150_in_transit: The charging cost of a HPC150 charging pole (in transit) per kWh in euro.
        :type HPC150_in_transit: float
        :param HPC150_at_home: The charging cost of a HPC150 charging pole (at home) per kWh in euro.
        :type HPC150_at_home: float
        :param HPC350_in_transit: The charging cost of a HPC350 charging pole (in transit) per kWh in euro.
        :type HPC350_in_transit: float
        :param HPC350_at_home: The charging cost of a HPC350 charging pole (at home) per kWh in euro.
        :type HPC350_at_home: float

        :return: An instance of a scenario year object.
        :rtype: ScenarioYear
        """

        self.year = year
        self.diesel_price_in_euro = diesel_price_in_euro
        self.electric_price_in_euro = electric_price_in_euro
        self.capacity_in_kWh = capacity_in_kWh
        self.repair_costs_EV_euro_per_year = repair_costs_EV_euro_per_year
        self.maintenance_costs_EV_euro_per_km = maintenance_costs_EV_euro_per_km
        self.maintenance_costs_diesel_euro_per_km = maintenance_costs_diesel_euro_per_km
        self.standstil_EV_in_days = standstil_EV_in_days
        self.subsidies_EV_in_euro = subsidies_EV_in_euro
        self.CO2_price_in_euro_per_ton = CO2_price_in_euro_per_ton
        self.efficiency_diesel_in_liter_per_km = efficiency_diesel_in_liter_per_km
        self.efficiency_electricity_in_kWh_per_km = efficiency_electricity_in_kWh_per_km
        self.electricity_price_private_excluding_tax_in_euro_per_kWh = electricity_price_private_excluding_tax_in_euro_per_kWh
        self.electricity_price_public_excluding_tax_in_euro_per_kWh = electricity_price_public_excluding_tax_in_euro_per_kWh
        self.gross_purchase_cost_charging_system_in_euro = gross_purchase_cost_charging_system_in_euro
        self.gross_installation_cost_charging_system_in_euro = gross_installation_cost_charging_system_in_euro
        self.fuel_price_diesel_excluding_tax_in_euro_per_liter = fuel_price_diesel_excluding_tax_in_euro_per_liter
        self.change_in_excise_duty_diesel_in_percentage = change_in_excise_duty_diesel_in_percentage
        self.vehicle_tax_diesel_in_euro_per_year = vehicle_tax_diesel_in_euro_per_year
        self.vehicle_tax_electric_in_euro_per_year = vehicle_tax_electric_in_euro_per_year
        self.MIA_in_euro_per_lifespan = MIA_in_euro_per_lifespan
        self.VAMIL_in_euro_per_lifespan = VAMIL_in_euro_per_lifespan
        self.energy_subsidy_in_euro_per_kWh = energy_subsidy_in_euro_per_kWh
        self.fixed_ZE_vehicle_tax_in_euro_per_year = fixed_ZE_vehicle_tax_in_euro_per_year
        self.difference_truck_toll_tax_in_euro_per_km = difference_truck_toll_tax_in_euro_per_km
        self.subsidy_charging_system_installation_in_euro_per_installation = \
            subsidy_charging_system_installation_in_euro_per_installation
        self.residual_value_EV_year_1_in_percentage = residual_value_EV_year_1_in_percentage
        self.residual_value_EV_year_2_in_percentage = residual_value_EV_year_2_in_percentage
        self.residual_value_EV_year_3_in_percentage = residual_value_EV_year_3_in_percentage
        self.residual_value_EV_year_4_in_percentage = residual_value_EV_year_4_in_percentage
        self.residual_value_EV_year_5_in_percentage = residual_value_EV_year_5_in_percentage
        self.residual_value_EV_year_6_in_percentage = residual_value_EV_year_6_in_percentage
        self.residual_value_EV_year_7_in_percentage = residual_value_EV_year_7_in_percentage
        self.residual_value_EV_year_8_in_percentage = residual_value_EV_year_8_in_percentage
        self.residual_value_EV_year_9_in_percentage = residual_value_EV_year_9_in_percentage
        self.residual_value_EV_year_10_in_percentage = residual_value_EV_year_10_in_percentage
        self.residual_value_EV_year_11_in_percentage = residual_value_EV_year_11_in_percentage
        self.residual_value_EV_year_12_in_percentage = residual_value_EV_year_12_in_percentage
        self.residual_value_EV_year_13_in_percentage = residual_value_EV_year_13_in_percentage
        self.residual_value_EV_year_14_in_percentage = residual_value_EV_year_14_in_percentage
        self.residual_value_EV_year_15_in_percentage = residual_value_EV_year_15_in_percentage
        self.residual_value_diesel_year_1_in_percentage = residual_value_diesel_year_1_in_percentage
        self.residual_value_diesel_year_2_in_percentage = residual_value_diesel_year_2_in_percentage
        self.residual_value_diesel_year_3_in_percentage = residual_value_diesel_year_3_in_percentage
        self.residual_value_diesel_year_4_in_percentage = residual_value_diesel_year_4_in_percentage
        self.residual_value_diesel_year_5_in_percentage = residual_value_diesel_year_5_in_percentage
        self.residual_value_diesel_year_6_in_percentage = residual_value_diesel_year_6_in_percentage
        self.residual_value_diesel_year_7_in_percentage = residual_value_diesel_year_7_in_percentage
        self.residual_value_diesel_year_8_in_percentage = residual_value_diesel_year_8_in_percentage
        self.residual_value_diesel_year_9_in_percentage = residual_value_diesel_year_9_in_percentage
        self.residual_value_diesel_year_10_in_percentage = residual_value_diesel_year_10_in_percentage
        self.residual_value_diesel_year_11_in_percentage = residual_value_diesel_year_11_in_percentage
        self.residual_value_diesel_year_12_in_percentage = residual_value_diesel_year_12_in_percentage
        self.residual_value_diesel_year_13_in_percentage = residual_value_diesel_year_13_in_percentage
        self.residual_value_diesel_year_14_in_percentage = residual_value_diesel_year_14_in_percentage
        self.residual_value_diesel_year_15_in_percentage = residual_value_diesel_year_15_in_percentage
        self.charging_capacity_external_charging_pole = charging_capacity_external_charging_pole
        self.charging_capacity_charging_pole_on_depot = charging_capacity_charging_pole_on_depot
        self.needed_charging_capacity_depot = needed_charging_capacity_depot
        self.needed_charging_capacity_in_transit = needed_charging_capacity_in_transit
        self.AC37_at_home = AC37_at_home
        self.AC10_in_transit = AC10_in_transit
        self.AC20_in_transit = AC20_in_transit
        self.AC20_at_home = AC20_at_home
        self.FC50_in_transit = FC50_in_transit
        self.FC50_at_home = FC50_at_home
        self.HPC150_in_transit = HPC150_in_transit
        self.HPC150_at_home = HPC150_at_home
        self.HPC350_in_transit = HPC350_in_transit
        self.HPC350_at_home = HPC350_at_home

    def to_dict(self):

        """Get the scenario year information as a dictionary.

        :return: The information about the scenario year.
        :rtype: dict
        """

        return {
            "year": self.year,
            "diesel_price_in_euro": self.diesel_price_in_euro,
            "electric_price_in_euro": self.electric_price_in_euro,
            "capacity_in_kWh": self.capacity_in_kWh,
            "repair_costs_EV_euro_per_year": self.repair_costs_EV_euro_per_year,
            "maintenance_costs_EV_euro_per_km": self.maintenance_costs_EV_euro_per_km,
            "maintenance_costs_diesel_euro_per_km": self.maintenance_costs_diesel_euro_per_km,
            "standstil_EV_in_days": self.standstil_EV_in_days,
            "subsidies_EV_in_euro": self.subsidies_EV_in_euro,
            "CO2_price_in_euro_per_ton": self.CO2_price_in_euro_per_ton,
            "efficiency_diesel_in_liter_per_km": self.efficiency_diesel_in_liter_per_km,
            "efficiency_electricity_in_kWh_per_km": self.efficiency_electricity_in_kWh_per_km,
            "electricity_price_private_excluding_tax_in_euro_per_kWh":
                self.electricity_price_private_excluding_tax_in_euro_per_kWh,
            "electricity_price_public_excluding_tax_in_euro_per_kWh":
                self.electricity_price_public_excluding_tax_in_euro_per_kWh,
            "gross_purchase_cost_charging_system_in_euro": self.gross_purchase_cost_charging_system_in_euro,
            "gross_installation_cost_charging_system_in_euro": self.gross_installation_cost_charging_system_in_euro,
            "fuel_price_diesel_excluding_tax_in_euro_per_liter": self.fuel_price_diesel_excluding_tax_in_euro_per_liter,
            "change_in_excise_duty_diesel_in_percentage": self.change_in_excise_duty_diesel_in_percentage,
            "vehicle_tax_diesel_in_euro_per_year": self.vehicle_tax_diesel_in_euro_per_year,
            "vehicle_tax_electric_in_euro_per_year": self.vehicle_tax_electric_in_euro_per_year,
            "MIA_in_euro_per_lifespan": self.MIA_in_euro_per_lifespan,
            "VAMIL_in_euro_per_lifespan": self.VAMIL_in_euro_per_lifespan,
            "energy_subsidy_in_euro_per_kWh": self.energy_subsidy_in_euro_per_kWh,
            "fixed_ZE_vehicle_tax_in_euro_per_year": self.fixed_ZE_vehicle_tax_in_euro_per_year,
            "difference_truck_toll_tax_in_euro_per_km": self.difference_truck_toll_tax_in_euro_per_km,
            "subsidy_charging_system_installation_in_euro_per_installation":
                self.subsidy_charging_system_installation_in_euro_per_installation,
            "residual_value_EV_year_1_in_percentage": self.residual_value_EV_year_1_in_percentage,
            "residual_value_EV_year_2_in_percentage": self.residual_value_EV_year_2_in_percentage,
            "residual_value_EV_year_3_in_percentage": self.residual_value_EV_year_3_in_percentage,
            "residual_value_EV_year_4_in_percentage": self.residual_value_EV_year_4_in_percentage,
            "residual_value_EV_year_5_in_percentage": self.residual_value_EV_year_5_in_percentage,
            "residual_value_EV_year_6_in_percentage": self.residual_value_EV_year_6_in_percentage,
            "residual_value_EV_year_7_in_percentage": self.residual_value_EV_year_7_in_percentage,
            "residual_value_EV_year_8_in_percentage": self.residual_value_EV_year_8_in_percentage,
            "residual_value_EV_year_9_in_percentage": self.residual_value_EV_year_9_in_percentage,
            "residual_value_EV_year_10_in_percentage": self.residual_value_EV_year_10_in_percentage,
            "residual_value_EV_year_11_in_percentage": self.residual_value_EV_year_11_in_percentage,
            "residual_value_EV_year_12_in_percentage": self.residual_value_EV_year_12_in_percentage,
            "residual_value_EV_year_13_in_percentage": self.residual_value_EV_year_13_in_percentage,
            "residual_value_EV_year_14_in_percentage": self.residual_value_EV_year_14_in_percentage,
            "residual_value_EV_year_15_in_percentage": self.residual_value_EV_year_15_in_percentage,
            "residual_value_diesel_year_1_in_percentage": self.residual_value_diesel_year_1_in_percentage,
            "residual_value_diesel_year_2_in_percentage": self.residual_value_diesel_year_2_in_percentage,
            "residual_value_diesel_year_3_in_percentage": self.residual_value_diesel_year_3_in_percentage,
            "residual_value_diesel_year_4_in_percentage": self.residual_value_diesel_year_4_in_percentage,
            "residual_value_diesel_year_5_in_percentage": self.residual_value_diesel_year_5_in_percentage,
            "residual_value_diesel_year_6_in_percentage": self.residual_value_diesel_year_6_in_percentage,
            "residual_value_diesel_year_7_in_percentage": self.residual_value_diesel_year_7_in_percentage,
            "residual_value_diesel_year_8_in_percentage": self.residual_value_diesel_year_8_in_percentage,
            "residual_value_diesel_year_9_in_percentage": self.residual_value_diesel_year_9_in_percentage,
            "residual_value_diesel_year_10_in_percentage": self.residual_value_diesel_year_10_in_percentage,
            "residual_value_diesel_year_11_in_percentage": self.residual_value_diesel_year_11_in_percentage,
            "residual_value_diesel_year_12_in_percentage": self.residual_value_diesel_year_12_in_percentage,
            "residual_value_diesel_year_13_in_percentage": self.residual_value_diesel_year_13_in_percentage,
            "residual_value_diesel_year_14_in_percentage": self.residual_value_diesel_year_14_in_percentage,
            "residual_value_diesel_year_15_in_percentage": self.residual_value_diesel_year_15_in_percentage,
            "charging_capacity_external_charging_pole": self.charging_capacity_external_charging_pole,
            "charging_capacity_charging_pole_on_depot": self.charging_capacity_charging_pole_on_depot,
            "needed_charging_capacity_depot": self.needed_charging_capacity_depot,
            "needed_charging_capacity_in_transit": self.needed_charging_capacity_in_transit,
            "AC37_at_home": self.AC37_at_home,
            "AC10_in_transit": self.AC10_in_transit,
            "AC20_in_transit": self.AC20_in_transit,
            "AC20_at_home": self.AC20_at_home,
            "FC50_in_transit": self.FC50_in_transit,
            "FC50_at_home": self.FC50_at_home,
            "HPC150_in_transit": self.HPC150_in_transit,
            "HPC150_at_home": self.HPC150_at_home,
            "HPC350_in_transit": self.HPC350_in_transit,
            "HPC350_at_home": self.HPC350_at_home
        }
