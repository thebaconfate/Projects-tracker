from flask import jsonify, make_response
from src.classes.customerrors.inputerror import InputException


class ErrorHandler:
    def __init__(self):
        # TODO add a logger to the constructor
        pass

    def __log_and_respond(self, dct, status_code):
        # TODO log the error to self.__logger
        return make_response(jsonify(dct), status_code)

    def handle(self, exception):
        match exception:
            case InputException():
                return self.__log_and_respond(
                    {"status": "error", "msg": exception.error_message}, 500
                )
            case _:
                return self.__log_and_respond(
                    {"status": "error", "msg": exception.__str__()}, 500
                )
