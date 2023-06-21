from Logger import Logger
from flask import Flask, render_template, request, Response
from request_functions import format_output, get_company_from_parameters, get_comparing_from_parameters, \
                              get_encoded_excel_from_body, get_fleet_data_from_parameters, get_json_data_from_body,\
                              get_output_from_parameters, get_scenario_data_from_parameters, \
                              get_scenarios_from_parameters, get_strategies_from_parameters, process_data
from waitress import serve

# Create app
app = Flask(__name__)

# Setup logger
logger = Logger(timezone_string="Europe/Amsterdam")


# Routes
@app.route("/")
def index():

    return render_template("index.html")


@app.route("/documentation")
def documentation():

    return render_template("documentation.html")


@app.route("/local_excel")
def process_local_excel():

    # Read input
    company = get_company_from_parameters(request)
    comparing = get_comparing_from_parameters(request)
    selected_scenarios = get_scenarios_from_parameters(request)
    selected_strategies = get_strategies_from_parameters(request)
    output = get_output_from_parameters(request)

    fleet_data = get_fleet_data_from_parameters(request, company)
    fleet = fleet_data["fleet"]

    scenario_data = get_scenario_data_from_parameters(request)
    scenarios = scenario_data["scenarios"]
    valid_scenario_names = scenario_data["scenario_names"]

    # Process data
    data = process_data(fleet,
                        scenarios,
                        valid_scenario_names,
                        output,
                        comparing,
                        selected_scenarios,
                        selected_strategies,
                        logger)
 
    # Return output
    output_format = request.args.get("output_format")
    return format_output(output_format, data)


@app.route("/external_excel", methods=["POST"])
def process_external_excel():

    # Read input
    company = get_company_from_parameters(request)
    comparing = get_comparing_from_parameters(request)
    selected_scenarios = get_scenarios_from_parameters(request)
    selected_strategies = get_strategies_from_parameters(request)
    output = get_output_from_parameters(request)

    excel_data = get_encoded_excel_from_body(request, company)
    fleet = excel_data["fleet"]
    scenarios = excel_data["scenarios"]
    valid_scenario_names = excel_data["scenario_names"]

    # Process data
    data = process_data(fleet,
                        scenarios,
                        valid_scenario_names,
                        output,
                        comparing,
                        selected_scenarios,
                        selected_strategies,
                        logger)

    # Return output
    output_format = request.args.get("output_format")
    return format_output(output_format, data)


@app.route("/json_data", methods=["POST"])
def process_json_data():

    # Read input
    comparing = get_comparing_from_parameters(request)
    selected_scenarios = get_scenarios_from_parameters(request)
    selected_strategies = get_strategies_from_parameters(request)
    output = get_output_from_parameters(request)

    json_data = get_json_data_from_body(request)
    fleet = json_data["fleet"]
    scenarios = json_data["scenarios"]
    valid_scenario_names = json_data["scenario_names"]

    # Process data
    data = process_data(fleet,
                        scenarios,
                        valid_scenario_names,
                        output,
                        comparing,
                        selected_scenarios,
                        selected_strategies,
                        logger)

    # Return output
    output_format = request.args.get("output_format")
    return format_output(output_format, data)


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

    # Print running message
    print("Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")

    # Serve app
    serve(app, host="127.0.0.1", port="5000")
