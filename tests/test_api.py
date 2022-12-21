from typing import Dict

import pytest
from httpx import AsyncClient, Response

from db.currency_db import CurrencyDB

from . import sample_rates as sr


@pytest.mark.asyncio
async def test_api_currencies_list(db: CurrencyDB, api: AsyncClient):

    await db.add_update(sr.base_currency, sr.rates)
    currencies: Response = await api.get("")

    json: Dict = currencies.json()
    success = json.get("success")

    assert success is not None and success is True
    assert json.get("currencies") == list(sr.rates.keys())


@pytest.mark.asyncio
async def test_latest_rate_for_currency_success(db: CurrencyDB, api: AsyncClient):

    await db.add_update(sr.base_currency, sr.rates)
    await db.add_update(sr.base_currency2, sr.rates2)

    curr_code = "AED"
    rate: Response = await api.get(f"/rates/{curr_code}")

    json: Dict = rate.json()
    success = json.get("success")

    assert success is not None and success is True
    assert json.get("currency_code") == curr_code
    assert json.get("base_currency") == sr.base_currency2
    assert json.get("rate") == sr.rates2[curr_code]


@pytest.mark.asyncio
async def test_currency_non_existant(db: CurrencyDB, api: AsyncClient):

    await db.add_update(sr.base_currency, sr.rates)

    curr_code = "ABC"

    rate: Response = await api.get(f"/rates/{curr_code}")

    json: Dict = rate.json()
    success = json.get("success")
    detail = json.get("detail")

    assert success is None
    assert detail is not None and detail == f"Currency code {curr_code} does not exist"
    assert rate.status_code == 404
