from datetime import datetime
from pytz import timezone, utc


def from_dict(data: dict):

    """Construct a vehicle from a dictionary.

    :param data: The input data.
    :type data: dict

    :return: The constructed vehicle.
    :rtype: Vehicle
    """

    vehicle = Vehicle(
        data["number_plate"],
        data["type"],
        data["category"],
        data["fuel_type"],
        data["euronorm"],
        data["year_of_purchase"],
        data["is_cooled"],
        data["PTO_fuel_consumption"],
        data["expected_total_distance_traveled_in_km"],
        data["maximum_daily_distance_in_km"],
        data["amount_of_operational_days"],
        data["drives_in_future_ZE_zone"],
        data["technological_lifespan"],
        data["loading_times"],
        data["charging_time_depot"],
        data["charging_time_public"],
        data["electricity_type"])

    return vehicle


class Vehicle:

    number_plate: str = None
    type: str = None
    category: int = None
    fuel_type: str = None
    euronorm: int = None
    year_of_purchase: int = None
    is_cooled: bool = None
    PTO_fuel_consumption: int = None
    expected_total_distance_traveled_in_km: int = None
    maximum_daily_distance_in_km: int = None
    amount_of_operational_days: int = None
    drives_in_future_ZE_zone: bool = None
    technological_lifespan: int = None
    loading_times: str = None
    charging_time_depot: int = None
    charging_time_public: int = None
    electricity_type: str = None

    def __init__(self,
                 number_plate: str,
                 vehicle_type: str,
                 category: int,
                 fuel_type: str,
                 euronorm: int,
                 year_of_purchase: int,
                 is_cooled: bool,
                 PTO_fuel_consumption: int,
                 expected_total_distance_traveled_in_km: int,
                 maximum_daily_distance_in_km: int,
                 amount_of_operational_days: int,
                 drives_in_future_ZE_zone: bool,
                 technological_lifespan: int,
                 loading_times: str,
                 charging_time_depot: int,
                 charging_time_public: int,
                 electricity_type: str):

        """Initialises a vehicle data object.

        :param number_plate: The number plate of the vehicle.
        :type number_plate: str
        :param vehicle_type: The type of the vehicle.
        :type vehicle_type: str
        :param category: The category of the vehicle.
        :type category: int
        :param fuel_type: The type of fuel that the vehicle uses.
        :type fuel_type: str
        :param euronorm: The euronorm of the vehicle. Euronorm (European Standard) is a technical standard
            for different commercial and industrial activities.
        :type euronorm: int
        :param year_of_purchase: The year that the vehicle was purchased.
        :type year_of_purchase: int
        :param is_cooled: Whether the vehicle is cooled or not.
        :type is_cooled: bool
        :param PTO_fuel_consumption: The PTO fuel consumption per day (in liters).
        :type PTO_fuel_consumption: int
        :param expected_total_distance_traveled_in_km: The expected distance that a vehicle has driven
            in it's lifetime.
        :type expected_total_distance_traveled_in_km: int
        :param maximum_daily_distance_in_km: The maximum distance that a vehicle drives in a day.
        :type maximum_daily_distance_in_km: int
        :param amount_of_operational_days: The amount of days that the vehicle is operational.
        :type amount_of_operational_days: int
        :param drives_in_future_ZE_zone: Whether the vehicle drives in a future ZE (Zero Emission) zone.
        :type drives_in_future_ZE_zone: bool
        :param flexible_planning: Whether the vehicle can drive on different routes.
        :type flexible_planning: bool
        :param technological_lifespan: The technological lifespan of the vehicle.
        :type technological_lifespan: int
        :param expected_residual_value_after_repayment: The expected residual value of the vehicle
            after all repayments have been made.
        :type expected_residual_value_after_repayment: int
        :param electricity_type: The type of electricity the vehicle use/would use, if it's electric.
        :type electricity_type: str

        :return: An instance of a vehicle object.
        :rtype: Vehicle
        """

        self.number_plate = number_plate
        self.type = vehicle_type
        self.category = category
        self.fuel_type = fuel_type
        self.euronorm = euronorm
        self.year_of_purchase = year_of_purchase
        self.is_cooled = is_cooled
        self.PTO_fuel_consumption = PTO_fuel_consumption
        self.expected_total_distance_traveled_in_km = expected_total_distance_traveled_in_km
        self.maximum_daily_distance_in_km = maximum_daily_distance_in_km
        self.amount_of_operational_days = amount_of_operational_days
        self.drives_in_future_ZE_zone = drives_in_future_ZE_zone
        self.technological_lifespan = technological_lifespan
        self.loading_times = loading_times
        self.charging_time_depot = charging_time_depot
        self.charging_time_public = charging_time_public
        self.electricity_type = electricity_type

    def get_current_age(self, tz: str = utc):

        """Get the current age of the vehicle in years.

        :param tz: The timezone that should be used to evaluate the age.
        :type tz: str

        :return: The age of the vehicle in years.
        :rtype: int
        """

        current_timestamp = datetime.now(timezone(tz))
        current_year = int(current_timestamp.strftime("%Y"))

        return current_year - self.year_of_purchase

    def to_dict(self):

        """Get the vehicle information as a dictionary.

        :return: The information about the vehicle.
        :rtype: dict
        """

        return {
            "number_plate": self.number_plate,
            "type": self.type,
            "category": self.category,
            "fuel_type": self.fuel_type,
            "euronorm": self.euronorm,
            "year_of_purchase": self.year_of_purchase,
            "is_cooled": self.is_cooled,
            "PTO_fuel_consumption": self.PTO_fuel_consumption,
            "expected_total_distance_traveled_in_km": self.expected_total_distance_traveled_in_km,
            "maximum_daily_distance_in_km": self.maximum_daily_distance_in_km,
            "amount_of_operational_days": self.amount_of_operational_days,
            "drives_in_future_ZE_zone": self.drives_in_future_ZE_zone,
            "technological_lifespan": self.technological_lifespan,
            "loading_times": self.loading_times,
            "charging_time_depot": self.charging_time_depot,
            "charging_time_public": self.charging_time_public,
            "electricity_type": self.electricity_type
        }
