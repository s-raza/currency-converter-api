import argparse
import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.currency_db import CurrencyDB
from db.models import Base
from db.utils import get_async_db, get_engine
from ext_api import CurrencyRatesDownloader, ExchangeRateAPI
from settings import settings as cfg
from utils import logger

updates_logger = logger.get_logger("CURRENCY UPDATES")


async def execute(freq_mins: int) -> None:
    """
    Execute the DB update.

    :param freq_mins: Interval in seconds for the update schedule.
    :type freq_mins: required

    :return: `None`
    """
    rates_api = ExchangeRateAPI()
    downloader = CurrencyRatesDownloader(rates_api)

    rates = downloader.get_rates()

    engine = await get_engine(cfg.db_conn_settings, Base)
    currency_db = await get_async_db(engine, CurrencyDB)  # type: ignore

    await currency_db.add_update(rates["base_currency"], rates["rates"])
    await currency_db.session.close()
    await engine.dispose()

    updates_logger.info(f"Database Updated, next update in {freq_mins} minutes")


if __name__ == "__main__":
    """
    Entry point for the currency rates DB updater.

    The interval in seconds for the update schedule can be provided on the command line
    using the `-m` switch. If it is not provided, the value of `UPDATER__FREQUENCY`
    from the `.env` file is used via the pydantic settings module.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--minutes", help="Frequency of updating currencies in minutes"
    )
    args = parser.parse_args()

    freq_mins = int(args.minutes) if args.minutes else cfg.updater.frequency

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        execute,
        "interval",
        minutes=freq_mins,
        args=[freq_mins],
        next_run_time=datetime.datetime.now(),
    )

    scheduler.start()
    asyncio.get_event_loop().run_forever()
