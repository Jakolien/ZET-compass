from database_interfaces.ScenarioDatabaseInterface import ScenarioDatabaseInterface
from data_objects.Scenario import from_dict as scenario_from_dict
from data_objects.Vehicle import from_dict as vehicle_from_dict
from excel_interfaces.FleetInterface import FleetInterface
from excel_interfaces.ScenariosInterface import ScenariosInterface
from flask import make_response, render_template, Request
from json import loads, dumps
from jsonschema import validate
from Logger import Logger
from TCOModel import TCOModel
from utility_functions import parameter_string_to_tupled_list, base64_decode_file

import exceptions as Exceptions
import os


def get_data_from_parameters(request: Request, parameter: str, on_not_valid: any=None, check: any=lambda x: True):
    """
    Get a parameter from the request URL parameters.

    Parameters:
        request (Request): The request.
        data (str): The parameter to retrieve.
        on_empty (str|Exception): The default value or exception to throw if the parameter is empty or not valid,
            defaults to None; if None, the parameter will be returned as is.
        check (Lambda): The function to call to check if the parameter is valid, defaults to lambda x: True.
    Returns:
        str: The parameter.
        any: The result of the on_empty function.

    Raises:
        Exception: The on_empty parameter when provided and the parameter is empty.
    """

    # Log the action
    Logger.warning(f"Retrieving {parameter} from parameters")
    
    # Get the data from the parameter
    data = request.args.get(parameter)
    
    # Check if the data is empty and if the on_empty parameter is specified
    if not (data and check(data)) and type(on_not_valid) in [Exception, str]:
        # Raise the exception if the on_empty parameter or exis an exception
        if type(on_not_valid) == Exception:
            raise on_not_valid

        # Execute the function if the on_empty parameter is a function
        data = on_not_valid
 
    # Return the data
    return data


def get_company_from_parameters(request: Request):
    """
    Get the company parameter from the request URL parameters.

    Parameters:
        request (Request): The request.

    Returns:
        str: The company parameter.

    Raises:
        NoCompanySpecified: The company parameter is not specified.
    """
     
    return get_data_from_parameters(request, "company", Exceptions.NoCompanySpecified)


def get_comparing_from_parameters(request: Request):
    """
    Get the comparing parameter from the request URL parameters.
    Defaults to "strategies".

    Parameters:
        request (Request): The request.

    Returns:
        str: The comparing parameter.
    """

    return get_data_from_parameters(request, "comparing", "strategies", lambda x: x in ["strategies", "scenarios"])


def get_scenarios_from_parameters(request: Request):
    """
    Get the scenarios parameter from the request URL parameters.
    Defaults to [ ].

    Parameters:
        request (Request): The request.

    Returns:
        str: The scenarios parameter.
    """

    data = get_data_from_parameters(request, "scenarios", "")
    return parameter_string_to_tupled_list(data)


def get_strategies_from_parameters(request: Request):
    """
    Get the strategies parameter from the request URL parameters.
    Defaults to [ ].

    Parameters:
        request (Request): The request.

    Returns:
        str: The strategies parameter.
    """

    data = get_data_from_parameters(request, "strategies", "")
    return parameter_string_to_tupled_list(data)


def get_output_from_parameters(request: Request):
    """
    Get the outputs from the request URL parameters.
    Defaults to ["graphs", "results"].

    Parameters:
    request (Request): The request.

    Returns:
    str: The outputs parameter.
    """

    data_array = get_data_from_parameters(request, "output", "graphs,results").split(",")
    actual_outputs = [output for output in data_array if output in ["graphs", "input", "results"]]
    return actual_outputs if len(actual_outputs) > 0 else ["graphs", "results"]


def get_fleet_data_from_parameters(request: Request, company: str):

    """
    Get the fleet data from the request URL parameters.

    Parameters:
        request (Request): The request.
        company (str): The company to get the fleet data for.

    Returns:
        tuple: The fleet data and errors. Both are provided as dictionaries.
    """

    path_to_fleet_data = get_data_from_parameters(request, "fleet_data", f"./input/wagenpark.xlsx")
    fleet_data = FleetInterface(company, path_to_fleet_data)
    return (fleet_data.fleet, fleet_data.errors)


def get_body(request: Request, error_on_empty: bool=True):
    """
    Get all data from the request body, formatted as json.

    Parameters:
        request (Request): The request.
        error_on_empty (bool): Whether to raise an error if the body is empty, defaults to True.

    Returns:
        dict: The data from the request body.

    Raises:
        RequestBodyInvalid: Raised if the request body is empty.
    """

    # Get the data from the request
    body = request.get_json(silent=True)

    # Check if there is any data present
    if body is None and error_on_empty:
        raise Exceptions.RequestBodyInvalid
    
    # Return the data of the body
    return body


def validate_body_with_schema(schema: str, body: dict, strict: bool=False):
    """
    Check whether the request body is valid JSON and matches with the validation schema.

    Parameters:
        schema (str): The name of the validation schema to be used.
        body (dict): The request body.
        strict (bool): Whether to raise an error if the request body is empty, defaults to False.

    Raises:
        NoSchemaFileFound: Raised if the validation schema does not exist and strict-mode is used.
    """

    # Check whether the schema exists, open it if it does
    if (os.path.exists(f"./validation_schemas/{schema}.json")):
        with open(f"./validation_schemas/{schema}.json", "r") as file:
            # Load the schema and validate the body
            schema = loads(file.read())
            validate(body, schema)

    # If the schema does not exist and strict is true, raise an error
    elif strict:
        raise Exceptions.NoSchemaFileFound


def get_excel_fleet_data_from_body(request: Request, company: str):
    """
    Gets the encoded Excel file containing the fleet data from the request body.

    Parameters:
        request (Request): The request.
        company (str): The company to be used

    Returns:
        array: The fleet data

    Raises:
        RequestBodyInvalid: Raised if the request body is not valid JSON.
        ValidationError: Raised if the request body does not match with the validation schema.
        
        See the "validation_schemas" directory and the json schema documentation for more details.
    """

    # Log the beginnen of the operation
    Logger.warning("Retrieving fleet data from provided Excel file")

    # Get the JSON data from the body and the check the validation schema
    body = get_body(request)
    validate_body_with_schema("external_excel", body)

    # Decode the base64 data into a temporary file and construct the fleet data
    fleet_file = base64_decode_file(body["fleet_data"]).name
    fleet_data = FleetInterface(company, fleet_file)

    # Get the fleet data and errors
    fleet = fleet_data.fleet
    errors = fleet_data.errors

    # Destroy the temporary file
    del fleet_data
    os.remove(fleet_file)

    return (fleet, errors)


def get_scenarios():
    """
    Gets the scenario data from the database.

    Returns:
        (dict, dict): The scenario data and the valid scenario names as a tuple
    """

    # Log the beginnen of the operation
    Logger.warning("Retrieving scenario data from the database")

    # Read the scenario data from the database
    scenarios = ScenarioDatabaseInterface().read_all_scenario_data()
    valid_scenario_names = ScenariosInterface.valid_scenario_names

    # Return the scenario data and the valid scenario names as tuple
    return (scenarios, valid_scenario_names)


def process_data(fleet: dict,
                 scenarios: dict,
                 valid_scenario_names: tuple,
                 output: tuple,
                 comparing: str,
                 selected_scenarios: tuple,
                 selected_strategies: tuple):

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

    Logger.warning("Processing data")

    # Initialise model
    model = TCOModel(fleet, scenarios, valid_scenario_names, output)

    # Process data
    data: dict = {}

    if comparing == "strategies":
        if len(selected_scenarios) < 1:
            raise Exceptions.NoScenarioSpecified
        else:
            if len(selected_strategies) < 1:
                selected_strategies = None
            data = model.compare_strategies(selected_scenarios[0], selected_strategies)

    elif comparing == "scenarios":
        if len(selected_strategies) < 1:
            raise Exceptions.NoStrategySpecified
        else:
            if len(selected_scenarios) < 1:
                selected_scenarios = None
            data = model.compare_scenarios(selected_strategies[0],  selected_scenarios)

    return data


def format_output(output_format: str, data: dict, errors: dict=None):
    """Format the model output.

    :param output_format: The format in which the results will be formatted.
    :type output_format: str
    :param data: The results of the TCO model.
    :type data: dict

    :raise OutputFormatIsNotSupported: Raised if an unknown format is specified.

    :return: The results in the specified format.
    :rtype: str or Response
    """

    Logger.warning("Formatting output")

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
                               scenario_year_properties=scenario_year_properties,
                               errors=errors)


    if output_format == "json":
        stringified_json = dumps(data, separators=(",", ":"))
        return make_response((stringified_json, 200, {"Content-Type": "application/json"}))

    # Raise error, if output mode isn't supported
    raise Exceptions.OutputFormatIsNotSupported
