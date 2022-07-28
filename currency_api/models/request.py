from typing import Optional


class CurrencyIn:
    def __init__(self, curr_code: str, on_date: Optional[str] = None):
        self.curr_code = curr_code
        self.on_date = on_date


class ConvertIn:
    def __init__(
        self, from_code: str, to_code: str, amount: float, on_date: Optional[str] = None
    ):
        self.from_code = from_code
        self.to_code = to_code
        self.amount = amount
        self.on_date = on_date
