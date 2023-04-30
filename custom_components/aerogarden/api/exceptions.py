
class AerogardenException(Exception):
    """ Base class for all other custom exceptions """
    pass

class AerogardenAuthFailedError(AerogardenException):
    """Error raised when the client failed to authenticate"""
    pass

class AerogardenServerError(AerogardenException):
    """Error raised when there is a server error (not 4xx http code)"""
    pass