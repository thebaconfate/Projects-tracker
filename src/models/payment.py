from pydantic import BaseModel, model_validator


class FloatPayment(BaseModel):
    amount: float = 0.0

    @model_validator(mode="after")
    def validate_amount(self):
        if self.amount < 0:
            raise ValueError("Amount must be positive")
        return self


class IntPayment(BaseModel):
    amount: int = 0
    cents: int = 0

    @model_validator(mode="after")
    def validate_amount(self):
        if self.amount < 0 or self.cents < 0:
            raise ValueError("Amount must be positive")
        return self
