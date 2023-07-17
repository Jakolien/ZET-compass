# Not supported
class OutputIsNotSupported(Exception):

    def __init__(self):

        super().__init__("The selected output is not supported. Please check the documentation.")


class OutputFormatIsNotSupported(Exception):

    def __init__(self):

        super().__init__("The selected output mode is not supported. Please check the documentation.")


# Not found
class NoExcelFileFound(Exception):

    def __init__(self):

        super().__init__("The specified excel file couldn't be found. Please check the path to the file.")


class NoSchemaFileFound(Exception):

    def __init__(self):

        super().__init__("The specified schema file couldn't be found and is required. Please check the path to the file.")


class NoFleetDataFound(Exception):

    def __init__(self):

        super().__init__("The fleet data couldn't be found. Please check the path to the fleet data.")


class NoScenarioDataFound(Exception):

    def __init__(self):

        super().__init__("The scenarios data couldn't be found. Please check the path to the scenarios data.")


class NoPANTEIAModelFound(Exception):

    def __init__(self):

        super().__init__("The PANTEIA model couldn't be found. Please check if the PANTEIA model still exists.")


class NoCompanySpecified(Exception):

    def __init__(self):

        super().__init__("The company couldn't be found. Please check the fleet data.")


class NoScenarioSpecified(Exception):

    def __init__(self):

        super().__init__("No scenario was specified. Please check the documentation.")


class NoStrategySpecified(Exception):

    def __init__(self):

        super().__init__("No strategy was specified. Please check the documentation.")


# Wrong input
class WrongInputType(Exception):

    def __init__(self):

        super().__init__("The type of the input is invalid. Please check the function description or documentation.")


class InvalidScenarioSpecified(Exception):

    def __init__(self):

        super().__init__("The specified scenario isn't valid. Please check the documentation.")


class InvalidStrategySpecified(Exception):

    def __init__(self):

        super().__init__("The specified strategy isn't valid. Please check the documentation.")


class RequestBodyInvalid(Exception):

    def __init__(self):

        super().__init__("The request has an invalid body. Please check the documentation.")


# Internal Error
class PANTEIAModelError(Exception):

    def __init__(self):

        super().__init__("Something went wrong with the PANTEIA model. Please check your input and the documentation.")


class NoDatabaseFileFound(Exception):

    def __init__(self):

        super().__init__("The database file couldn't be found. Please check the path to the database file.")
