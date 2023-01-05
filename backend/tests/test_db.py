import pytest

from db.currency_db import CurrencyDB

from . import sample_rates as sr


@pytest.mark.asyncio
async def test_currency_codes(db: CurrencyDB):

    await db.add_update(sr.base_currency, sr.rates)
    diff = set(list(sr.rates.keys())) ^ set(await db.get_currency_codes())
    assert not diff


@pytest.mark.asyncio
async def test_last_update(db: CurrencyDB):

    current = await db.last_update_date

    if not current:
        current_last_update_id = 0
    else:
        current_last_update_id = current.id

    await db.add_update(sr.base_currency, sr.rates)
    last_udpate_date = await db.last_update_date
    assert current_last_update_id + 1 == last_udpate_date.id


@pytest.mark.asyncio
async def test_all_latest_rates_correct(db: CurrencyDB):

    await db.add_update(sr.base_currency, sr.rates)
    latest_rates = await db.get_currency_rates()
    assert latest_rates["rates"] == sr.rates


@pytest.mark.asyncio
async def test_latest_rate_correct(db: CurrencyDB):

    curr_code = "AED"

    await db.add_update(sr.base_currency2, sr.rates2)
    latest_rate = await db.get_rate_on_date(curr_code)
    assert latest_rate.rate == sr.rates2[curr_code]


@pytest.mark.asyncio
async def test_latest_rate_curr_non_existant(db: CurrencyDB):

    curr_code = "ABC"

    await db.add_update(sr.base_currency2, sr.rates2)

    with pytest.raises(ValueError, match=r".*Currency code .* does not exist.*"):
        await db.get_rate_on_date(curr_code)


@pytest.mark.asyncio
async def test_rate_on_date_correct(db: CurrencyDB):

    test_date = "01-08-2022"
    curr_code = "AED"

    await db.add_update(sr.base_currency2, sr.rates2, test_date)
    rate_on_date = await db.get_rate_on_date(curr_code, test_date)
    assert rate_on_date.rate == sr.rates2[curr_code]


@pytest.mark.asyncio
async def test_add_update_wrong_date_exception(db: CurrencyDB):

    wrong_date_format = "2022-08-2022"

    with pytest.raises(ValueError, match=r"Malformed date format.*"):
        await db.add_update(sr.base_currency2, sr.rates2, wrong_date_format)


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

    rates = sr.sample_rates2["rates"]

    from_rate = rates[from_curr_code]
    to_rate = rates[to_curr_code]
    amount = 1

    converted = (to_rate / from_rate) * amount

    await db.add_update(sr.base_currency2, sr.rates2)
    from_db = await db.convert_rate(from_curr_code, to_curr_code, amount)
    assert from_db["converted"] == converted
