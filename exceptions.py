class NotFoundException(Exception):
    pass


# class InvalidArgumentException(Exception):
#     pass


class UnauthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class InvalidArgumentException(ValueError):
    pass

class ApiNotFoundException(ValueError):
    pass

class InvalidMethodException(ValueError):
    pass    



class UnauthorizedException(Exception):
    def __init__(self, message="Необходимо авторизоваться", realm="api"):
        super().__init__(message)
        self.realm = realm


