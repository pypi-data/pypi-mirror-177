class InvalidDirectionError(Exception):
    """Exception thrown for an invalid bus/train direction"""

    def __init__(self, direction_provided: str, message: str = None):
        if not message:
            message = f'{direction_provided} is an invalid direction.'
        super(Exception, self).__init__(message)


class InvalidVehicleTypeError(Exception):
    """Exception thrown for an invalid vehicle type"""

    def __init__(self, vehicle_type_provided: str, message: str = None):
        if not message:
            message = f'{vehicle_type_provided} is an invalid vehicle type.'
        super(Exception, self).__init__(message)


class InvalidTrainLineError(Exception):
    """Exception thrown for an invalid train line"""

    def __init__(self, line_provided: str, message: str = None):
        if not message:
            message = f'{line_provided} is an invalid train line.'
        super(Exception, self).__init__(message)


class InvalidTrainLineCodeError(Exception):
    """Exception thrown for an invalid train line code"""

    def __init__(self, line_code_provided: str, message: str = None):
        if not message:
            message = f'{line_code_provided} is an invalid train line code.'
        super(Exception, self).__init__(message)
