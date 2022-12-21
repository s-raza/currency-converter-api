from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class CurrencyRateResponse(BaseModel):
    success: bool
    currency_code: str
    base_currency: str
    rate: float
    last_updated: datetime


class ConvertedResponse(BaseModel):
    success: bool
    from_currency_code: str
    to_currency_code: str
    amount: float
    converted: float
    base_currency: str
    last_updated: datetime


class CurrenciesResponse(BaseModel):
    success: bool
    currencies: List[str]


class CurrenciesRatesResponse(BaseModel):
    created: datetime
    base_currency: str
    rates: Dict[str, float]
