from Logger import Logger
from flask import Flask, render_template, request, Response
from waitress import serve

import request_functions as helper

# Create app
app = Flask(__name__)

# Routes
@app.route("/")
def index():
    """
    Render the index page.

    Returns:
        str: The index page.
    """

    Logger.warning("Request: Index Page")
    return render_template("index.html")


@app.route("/documentation")
def documentation():
    """
    Render the documentation page

    Returns:
        str: The documentation page.
    """

    Logger.warning("Request: Documentation")
    return render_template("documentation.html")


@app.route("/local_excel")
def process_local_excel():
    """
    Process the local excel files and return the predictions

    Returns:
        str: The predictions.
    """

    # Log the request
    Logger.warning("Request: Local Excel Analyses")

    # Read input
    Logger.warning("Processing parameters")
    company = helper.get_company_from_parameters(request)
    comparing = helper.get_comparing_from_parameters(request)
    selected_scenarios = helper.get_scenarios_from_parameters(request)
    selected_strategies = helper.get_strategies_from_parameters(request)
    output = helper.get_output_from_parameters(request)

    Logger.warning("Processing fleet data")
    fleet, fleet_errors = helper.get_fleet_data_from_parameters(request, company)

    Logger.warning("Processing scenario data")
    scenarios, valid_scenario_names = helper.get_scenarios()

    # Process data
    data = helper.process_data(fleet,
                        scenarios,
                        valid_scenario_names,
                        output,
                        comparing,
                        selected_scenarios,
                        selected_strategies)
 
    # Return output
    output_format = request.args.get("output_format")
    return helper.format_output(output_format, data, fleet_errors)


@app.route("/external_excel", methods=["POST"])
def process_external_excel():

    # Read input
    Logger.warning("Processing parameters")
    company = helper.get_company_from_parameters(request)
    comparing = helper.get_comparing_from_parameters(request)
    selected_scenarios = helper.get_scenarios_from_parameters(request)
    selected_strategies = helper.get_strategies_from_parameters(request)
    output = helper.get_output_from_parameters(request)

    # Get the fleet and scenario data
    fleet, fleet_errors = helper.get_excel_fleet_data_from_body(request, company)
    scenarios, valid_scenario_names = helper.get_scenarios()

    # Process data
    Logger.warning("Predicting")
    data = helper.process_data(
        fleet,
        scenarios,
        valid_scenario_names,
        output,
        comparing,
        selected_scenarios,
        selected_strategies
    )

    # Return output
    Logger.warning("Outputting")
    output_format = request.args.get("output_format")
    return helper.format_output(output_format, data, fleet_errors)


@app.route("/json_data", methods=["POST"])
def process_json_data():

    # Read input
    comparing = helper.get_comparing_from_parameters(request)
    selected_scenarios = helper.get_scenarios_from_parameters(request)
    selected_strategies = helper.get_strategies_from_parameters(request)
    output = helper.get_output_from_parameters(request)

    json_data = helper.get_json_data_from_body(request)
    fleet = json_data["fleet"]
    scenarios = json_data["scenarios"]
    valid_scenario_names = json_data["scenario_names"]

    # Process data
    data = helper.process_data(fleet,
                        scenarios,
                        valid_scenario_names,
                        output,
                        comparing,
                        selected_scenarios,
                        selected_strategies)

    # Return output
    output_format = request.args.get("output_format")
    return helper.format_output(output_format, data)


@app.errorhandler(403)
def return_forbidden_response(exception):

    return Response(response=render_template("exception.html",
                                             exception=exception,
                                             message="You are not allowed to access this site. "
                                                     "If this is incorrect, please contact an administrator."),
                    status=403,
                    mimetype="text/html")


@app.errorhandler(404)
def return_not_found_response(exception):

    return Response(response=render_template("exception.html",
                                             exception=exception,
                                             message="This page doesn't exist. "
                                                     "The page may have been moved or you may have misspelled it."),
                    status=404,
                    mimetype="text/html")


@app.errorhandler(500)
def return_error_response(exception):

    if exception.original_exception is not None:
        name = type(exception.original_exception).__name__
        message = exception.original_exception
    else:
        name = exception.name
        message = exception
    return Response(render_template("exception.html",
                                    exception=name,
                                    message=message),
                    status=500,
                    mimetype="text/html")


if __name__ == "__main__":

    # Setup logger 
    Logger.initialize(timezone_string="Europe/Amsterdam", level="WARNING")

    # Print running message
    print("Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")

    # Serve app
    serve(app, host="127.0.0.1", port="5000")
