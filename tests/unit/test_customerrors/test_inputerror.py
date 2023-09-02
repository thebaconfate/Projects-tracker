import pytest
from src.classes.customerrors.inputerror import InputException

error_msg = "Input Error"


class TestInputException:
    def test_input_exception(self):
        with pytest.raises(InputException):
            raise InputException(error_msg)

    def test_input_exception_message(self):
        input_exception = InputException(error_msg)
        assert input_exception.error_message == error_msg
