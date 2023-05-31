from data_objects.ScenarioYear import from_dict as year_from_dict


def from_dict(data: dict):

    """Construct a scenario from a dictionary.

    :param data: The input data.
    :type data: dict

    :return: The constructed scenario.
    :rtype: Scenario
    """

    years = {int(year): year_from_dict(year_data) for year, year_data in data["years"].items()}
    scenario = Scenario(data["name"],
                        data["scenario_type"],
                        data["vehicle_type"],
                        years)

    return scenario


class Scenario:

    name: str = None
    scenario_type: str = None
    vehicle_type: str = None
    years: dict = None

    def __init__(self,
                 name: str,
                 scenario_type: str,
                 vehicle_type: str,
                 years: dict):

        """Initialises a scenario data object.

        :param name: The name of the scenario. Consists of the scenario type and vehicle type. Example: "hoog N1".
        :type: str
        :param scenario_type: The type of scenario.
        :type: str
        :param vehicle_type: The vehicle type this scenarios belongs to.
        :type: str
        :param years: The scenario data organised by year in a dictionary.
        :type: dict

        :return: An instance of a scenario object.
        :rtype: Scenario
        """

        self.name = name
        self.scenario_type = scenario_type
        self.vehicle_type = vehicle_type
        self.years = years

    def to_dict(self):

        """Get the scenario information as a dictionary.

        :return: The information about the scenario.
        :rtype: dict
        """

        years = {year: year_data.to_dict() for year, year_data in self.years.items()}

        return {
            "name": self.name,
            "scenario_type": self.scenario_type,
            "vehicle_type": self.vehicle_type,
            "years": years
        }
