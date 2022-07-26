import pytest

from db.currency_db import CurrencyDB

from .sample_rates import sample_rates, sample_rates2

base_currency = sample_rates["base_currency"]
rates = sample_rates["rates"]

base_currency2 = sample_rates2["base_currency"]
rates2 = sample_rates2["rates"]


@pytest.mark.asyncio
async def test_currency_codes(db: CurrencyDB):

    await db.add_update(base_currency, rates)
    diff = set(list(rates.keys())) ^ set(await db.get_currency_codes())
    assert not diff


@pytest.mark.asyncio
async def test_last_update(db: CurrencyDB):

    await db.add_update(base_currency, rates)
    last_udpate_date = await db.last_update_date
    assert last_udpate_date.id == 2


@pytest.mark.asyncio
async def test_latest_rate_correct(db: CurrencyDB):

    curr_code = "AED"

    await db.add_update(base_currency2, rates2)
    latest_rate = await db.get_rate_on_date(curr_code)
    assert latest_rate.rate == rates2[curr_code]


@pytest.mark.asyncio
async def test_latest_rate_curr_non_existant(db: CurrencyDB):

    curr_code = "ABC"

    await db.add_update(base_currency2, rates2)

    with pytest.raises(ValueError, match=r".*Currency code .* does not exist.*"):
        await db.get_rate_on_date(curr_code)


@pytest.mark.asyncio
async def test_rate_on_date_correct(db: CurrencyDB):

    test_date = "01-08-2022"
    curr_code = "AED"

    await db.add_update(base_currency2, rates2, test_date)
    rate_on_date = await db.get_rate_on_date(curr_code, test_date)
    assert rate_on_date.rate == rates2[curr_code]


@pytest.mark.asyncio
async def test_add_update_wrong_date_exception(db: CurrencyDB):

    wrong_date_format = "2022-08-2022"

    with pytest.raises(ValueError, match=r"Malformed date format.*"):
        await db.add_update(base_currency2, rates2, wrong_date_format)


@pytest.mark.asyncio
async def test_get_rate_on_date_wrong_date_exception(db: CurrencyDB):

    wrong_date_format = "2022-08-2022"
    curr_code = "AED"

    with pytest.raises(ValueError, match=r"Malformed date format.*"):
        await db.get_rate_on_date(curr_code, wrong_date_format)


@pytest.mark.asyncio
async def test_currency_conversion(db: CurrencyDB):

    from_curr_code = "AED"
    to_curr_code = "INR"

    rates = sample_rates2["rates"]

    from_rate = rates[from_curr_code]
    to_rate = rates[to_curr_code]
    amount = 1

    converted = (to_rate / from_rate) * amount

    await db.add_update(base_currency2, rates2)
    from_db = await db.convert_rate(from_curr_code, to_curr_code, amount)
    assert from_db["converted"] == converted
