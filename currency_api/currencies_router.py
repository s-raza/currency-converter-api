from typing import Any, Dict, List, Union

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from db.currency_db import CurrencyDB
from db.models import CurrencyUpdates

from .dependencies.db import get_currency_db
from .user_auth_router import UserModel, get_current_active_user

currencies_router = APIRouter()


async def close_conn(conn: CurrencyDB) -> None:
    await conn.session.close()
    await conn.engine.dispose()


@currencies_router.get("/currencies/rate/{curr_code}")
async def get_currency_code_rate(
    curr_code: str,
    background_tasks: BackgroundTasks,
    on_date: Union[str, None] = None,
    currency_db: CurrencyDB = Depends(get_currency_db),
    auth_user: UserModel = Depends(get_current_active_user),
) -> Dict[str, Any]:

    background_tasks.add_task(close_conn, currency_db)
    try:
        currency: CurrencyUpdates = await currency_db.get_rate_on_date(
            curr_code, on_date
        )
    except ValueError as e:
        errcode, errtxt = e.args[0]
        raise HTTPException(status_code=errcode, detail=errtxt)
    await currency_db.session.close()
    return {
        "success": True,
        "currency_code": curr_code,
        "base_currency": currency.date_updated.base_currency.code,
        "rate": currency.rate,
        "last_updated": currency.date_updated.created,
    }


@currencies_router.get("/currencies/convert/{from_code}/{to_code}")
async def convert_currency_rate(
    from_code: str,
    to_code: str,
    amount: float,
    background_tasks: BackgroundTasks,
    on_date: Union[str, None] = None,
    currency_db: CurrencyDB = Depends(get_currency_db),
    auth_user: UserModel = Depends(get_current_active_user),
) -> Dict[str, Any]:

    background_tasks.add_task(close_conn, currency_db)
    try:
        converted: Dict[str, Any] = await currency_db.convert_rate(
            from_code, to_code, amount, on_date
        )
    except ValueError as e:
        errcode, errtxt = e.args[0]
        raise HTTPException(status_code=errcode, detail=errtxt)

    await currency_db.session.close()
    return {
        "success": True,
        "from_currency_code": from_code,
        "to_currency_code": to_code,
        "amount": amount,
        **converted,
    }


@currencies_router.get("/currencies")
async def get_all_currencies(
    background_tasks: BackgroundTasks,
    currency_db: CurrencyDB = Depends(get_currency_db),
    auth_user: UserModel = Depends(get_current_active_user),
) -> Dict[str, Any]:

    background_tasks.add_task(close_conn, currency_db)
    currencies: List[str] = await currency_db.get_currency_codes()
    await currency_db.session.close()
    return {"success": True, "currencies": currencies}
