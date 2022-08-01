from typing import Dict

import pytest
from httpx import AsyncClient, Response

from db.currency_db import CurrencyDB

from . import sample_rates as sr


@pytest.mark.asyncio
async def test_api_currencies_list(db: CurrencyDB, api: AsyncClient):

    await db.add_update(sr.base_currency, sr.rates)
    currencies: Response = await api.get("/")

    json: Dict = currencies.json()
    success = json.get("success")

    assert success is not None and success is True
    assert json.get("currencies") == list(sr.rates.keys())
