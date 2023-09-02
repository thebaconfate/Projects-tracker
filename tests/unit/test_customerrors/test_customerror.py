import pytest
from src.classes.customerrors.customerror import CustomError

error_msg = "custom error"


class TestCustomErros:
    def test_custom_error(self):
        with pytest.raises(CustomError):
            raise CustomError(error_msg)

    def test_custom_error_msg(self):
        customerror = CustomError(error_msg)
        assert customerror.error_message == error_msg
