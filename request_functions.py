from data_objects.Scenario import from_dict as scenario_from_dict
from data_objects.Vehicle import from_dict as vehicle_from_dict
from excel_interfaces.FleetInterface import FleetInterface
from excel_interfaces.ScenariosInterface import ScenariosInterface
from exceptions import NoCompanySpecified, NoScenarioSpecified, NoStrategySpecified, OutputFormatIsNotSupported, \
                       RequestBodyInvalid
from flask import make_response, render_template, Request, Response
from json import loads, dumps
from jsonschema import validate
from Logger import Logger
from TCOModel import TCOModel
from utility_functions import base64_decode_file


def get_company_from_parameters(request: Request):

    """Get the company parameter from the request URL parameters.

    :param request: The request.
    :type request: Request

    :raise NoCompanySpecified: Raised if the parameter is not present or empty.

    :return: The company parameter.
    :rtype: str
    """

    company = request.args.get("company")
    if company is None and \
       company != "":
        raise NoCompanySpecified

    return company


def get_comparing_from_parameters(request: Request):

    """Get the comparing parameter from the request URL parameters.

    :param request: The request.
    :type request: Request

    :return: The comparing parameter.
    :rtype: str
    """

    comparing = request.args.get("comparing")
    if comparing not in ["strategies", "scenarios"]:
        comparing = "strategies"

    return comparing


def get_scenarios_from_parameters(request: Request):

    """Get the scenarios parameter from the request URL parameters.

    :param request: The request.
    :type request: Request

    :return: The scenarios parameter.
    :rtype: tuple
    """

    scenarios = request.args.get("scenarios")
    if scenarios is not None and \
            scenarios != "":
        scenarios = scenarios.split(",")
    else:
        scenarios = []

    # Make list into read only tuple
    scenarios = tuple(scenarios,)

    return scenarios


def get_strategies_from_parameters(request: Request):

    """Get the strategies parameter from the request URL parameters.

    :param request: The request.
    :type request: Request

    :return: The strategies parameter.
    :rtype: tuple
    """

    strategies = request.args.get("strategies")
    if strategies is not None and \
       strategies != "":
        strategies = strategies.split(",")
    else:
        strategies = []

    # Make list into read only tuple
    strategies = tuple(strategies,)

    return strategies


def get_output_from_parameters(request: Request):

    """Get the outputs from the request URL parameters.

    :param request: The request.
    :type request: Request

    :return: A tuple with the valid outputs. Defaults to "graphs" and "results", if there are none.
    :rtype: tuple
    """

    # Get output parameter and check for valid outputs
    output_parameter = request.args.get("output", "")
    outputs = output_parameter.split(",")
    actual_outputs = [output for output in outputs if output in ["graphs", "input", "results"]]

    # If there are no valid outputs, default to graphs and table results
    if len(actual_outputs) < 1:
        actual_outputs = ["graphs", "results"]

    # Turn list into tuple
    actual_outputs = tuple(actual_outputs)

    return actual_outputs


def get_fleet_data_from_parameters(request: Request, company: str):

    """Get the fleet data from the request URL parameters.

    :param request: The request.
    :type request: Request
    :param company: The company to be used for the FleetInterface.
    :type company: str

    :return: The scenario Excel data in dictionary format. Consists of: path, interface, and fleet.
    :rtype: dict
    """

    path_to_fleet_data = request.args.get("fleet_data")
    if path_to_fleet_data is None:
        path_to_fleet_data = "./input/wagenpark.xlsx"

    fleet_interface = FleetInterface(company, path_to_fleet_data)
    fleet = fleet_interface.fleet

    return {
        "path": path_to_fleet_data,
        "interface": fleet_interface,
        "fleet": fleet
    }


def get_scenario_data_from_parameters(request: Request):

    """Get the scenario data from the request URL parameters.

    :param request: The request.
    :type request: Request

    :return: The scenario Excel data in dictionary format. Consists of: path, interface, scenarios, and scenario_names.
    :rtype: dict
    """

    path_to_scenario_data = request.args.get("scenario_data")
    if path_to_scenario_data is None:
        path_to_scenario_data = "./input/scenarios.xlsx"

    scenarios_interface = ScenariosInterface(path_to_scenario_data)
    scenarios = scenarios_interface.scenarios
    valid_scenario_names = scenarios_interface.valid_scenario_names

    return {
        "path": path_to_scenario_data,
        "interface": scenarios_interface,
        "scenarios": scenarios,
        "scenario_names": valid_scenario_names
    }


def get_json_data_from_body(request: Request):

    """Gets the JSON input data from the request body.

    :param request: The request.
    :type request: Request

    :raise RequestBodyInvalid: Raised if the request body is not valid JSON.
    :raise ValidationError: Raised if the request body does not match with the validation schema.
        See the "validation_schemas" directory and the json schema documentation for more details.

    :return: The JSON data in dictionary format. Consists of: fleet, scenarios, and scenario_names.
    :rtype: dict
    """

    # Get JSON data
    body = request.get_json()
    if body is None:
        raise RequestBodyInvalid

    # Get validation schema
    try:
        with open("./validation_schemas/json_data.json", "r") as file:
            schema = loads(file.read())
    except:
        schema = None

    # Get and check data
    # Skip checking if schema can't be found
    if schema is not None:
        validate(body, schema)

    fleet = {number_plate: vehicle_from_dict(vehicle) for number_plate, vehicle in body["fleet"].items()}
    scenarios = {scenario_name: {vehicle_type: scenario_from_dict(scenario_data)
                                 for vehicle_type, scenario_data in vehicle_types.items()}
                 for scenario_name, vehicle_types in body["scenarios"].items()}
    valid_scenario_names = (
        "laag",
        "midden",
        "hoog"
    )

    return {
        "fleet": fleet,
        "scenarios": scenarios,
        "scenario_names": valid_scenario_names
    }


def get_encoded_excel_from_body(request: Request, company: str):

    """Gets the encoded Excel files from the request body.

    :param request: The request.
    :type request: Request
    :param company: The company to be used for the FleetInterface.
    :type company: str

    :raise RequestBodyInvalid: Raised if the request body is not valid JSON.
    :raise ValidationError: Raised if the request body does not match with the validation schema.
        See the "validation_schemas" directory and the json schema documentation for more details.

    :return: The Excel data in dictionary format. Consists of: fleet, scenarios, and scenario_names.
    :rtype: dict
    """

    # Get JSON data
    body = request.get_json(silent=True)
    if body is None:
        raise RequestBodyInvalid

    # Get validation schema
    try:
        with open("./validation_schemas/external_excel.json", "r") as file:
            schema = loads(file.read())
    except:
        schema = None

    # Get and check data
    # Skip checking if schema can't be found
    if schema is not None:
        validate(body, schema)

    # Decode base64 into temporary files
    fleet_temp = base64_decode_file(body["fleet_data"])
    scenario_temp = base64_decode_file(body["scenario_data"])

    # Construct interfaces and get data
    fleet_interface = FleetInterface(company, fleet_temp.name)
    fleet = fleet_interface.fleet

    scenarios_interface = ScenariosInterface(scenario_temp.name)
    scenarios = scenarios_interface.scenarios
    valid_scenario_names = scenarios_interface.valid_scenario_names

    return {
        "fleet": fleet,
        "scenarios": scenarios,
        "scenario_names": valid_scenario_names
    }


def process_data(fleet: dict,
                 scenarios: dict,
                 valid_scenario_names: tuple,
                 output: tuple,
                 comparing: str,
                 selected_scenarios: tuple,
                 selected_strategies: tuple,
                 logger: Logger):

    """Processes the input data using the TCO Model.

    :param fleet: The fleet data.
    :type fleet: dict
    :param scenarios: The scenario data.
    :type scenarios: dict
    :param valid_scenario_names: The valid scenario names.
    :type valid_scenario_names: tuple
    :param output: The specified output.
    :type output: tuple
    :param comparing: The specified comparison mode.
    :type comparing: str
    :param selected_scenarios: The selected scenarios.
    :type selected_scenarios: tuple
    :param selected_strategies: The selected strategies.
    :type selected_strategies: tuple,
    :param logger: The logger to allow for logging.
    :type logger: Logger

    :raise NoScenarioSpecified: Raised if the comparison mode is "strategies", but no scenario is specified.
    :raise NoStrategySpecified: Raised if the comparison mode is "scenarios", but no strategy is specified.

    :return: The results of the TCO Model. This depends on the output parameter.
    :rtype: dict
    """

    # Initialise model
    model = TCOModel(fleet, scenarios, valid_scenario_names, output, logger)

    # Process data
    data: dict = {}

    if comparing == "strategies":
        if len(selected_scenarios) < 1:
            raise NoScenarioSpecified
        else:
            if len(selected_strategies) < 1:
                selected_strategies = None
            data = model.compare_strategies(selected_scenarios[0], logger, selected_strategies)

    elif comparing == "scenarios":
        if len(selected_strategies) < 1:
            raise NoStrategySpecified
        else:
            if len(selected_scenarios) < 1:
                selected_scenarios = None
            data = model.compare_scenarios(selected_strategies[0], logger,  selected_scenarios)

    return data


def format_output(output_format: str, data: dict):

    """Format the model output.

    :param output_format: The format in which the results will be formatted.
    :type output_format: str
    :param data: The results of the TCO model.
    :type data: dict

    :raise OutputFormatIsNotSupported: Raised if an unknown format is specified.

    :return: The results in the specified format.
    :rtype: str or Response
    """

    # Define accepted output formats
    output_formats = [
        "html",
        "json"
    ]

    # If output mode is invalid, then default to html
    if output_format not in output_formats:
        output_format = "html"

    # Return results
    if output_format == "html":

        result_properties = None
        if data.get("results", None):
            result_properties = \
                list(
                    list(
                        list(data["results"]["sum"].values()
                        )[0].values()
                    )[0].values()
                )[0].keys()

        fleet_properties = None
        if data.get("original_fleet", None):
            fleet_properties = list(data["original_fleet"].values())[0].keys()

        scenario_year_properties = None
        if data.get("scenarios"):
            scenario_year_properties = \
                list(
                    list(
                        list(data["scenarios"].values()
                         )[0].values()
                    )[0]["years"].values()
                )[0].keys()

        return render_template("results.html",
                               data=data,
                               result_properties=result_properties,
                               fleet_properties=fleet_properties,
                               scenario_year_properties=scenario_year_properties)


    if output_format == "json":
        stringified_json = dumps(data, separators=(",", ":"))
        return make_response((stringified_json, 200, {"Content-Type": "application/json"}))

    # Raise error, if output mode isn't supported
    raise OutputFormatIsNotSupported
