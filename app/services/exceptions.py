#user exceptions:
class UserDoesNotExistException(Exception):
    pass

#product exceptions:
class ProductUnavailableException(Exception):
    pass


class NoProductFoundException(Exception):
    pass

class InvalidInputException(Exception):
    pass

class DuplicateProductException(Exception):
    pass

class DatabaseOperationException(Exception):
    pass

class BadRequestException(Exception):
    pass