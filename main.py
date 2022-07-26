import asyncio


from db.currency_db import CurrencyDB
from db.models import Base

# from db.utils import get_engine
from db.utils import get_async_db, get_engine
from settings import settings as cfg
from tests.sample_rates import sample_rates


async def main():

    engine = await get_engine(cfg.db_conn_settings, Base)
    currency_db = await get_async_db(engine, CurrencyDB)
    print(f"{currency_db =}")
    await currency_db.add_update(sample_rates["base_currency"], sample_rates["rates"])

    latest_rate = await currency_db.get_latest_rate("INR")
    print(f"{latest_rate = }")

    rate_on_date = await currency_db.get_rate_on_date("INR", "22-07-2022")
    print(f"{rate_on_date = }")

    all_currencies = await currency_db.get_currency_codes()
    print(f"{len(all_currencies) = }")

    last_update_date = await currency_db.last_update_date
    print(f"{last_update_date = }")

    await currency_db.session.close()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # asyncio.run(main())
