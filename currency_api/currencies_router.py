from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from db.currency_db import CurrencyDB
from db.models import CurrencyUpdates

from .dependencies.db import get_currency_db
from .models import errors as err
from .models import request as req
from .models import response as resp
from .user_auth_router import UserModel, get_current_active_user

currencies_router = APIRouter()


@currencies_router.get(
    "/rate/{curr_code}",
    response_model=resp.CurrencyRateResponse,
    responses=err.get_responses(err.all_errors),
)
async def get_currency_code_rate(
    currency_in: req.CurrencyIn = Depends(),
    currency_db: CurrencyDB = Depends(get_currency_db),
    auth_user: UserModel = Depends(get_current_active_user),
) -> Dict[str, Any]:

    try:
        db: CurrencyUpdates = await currency_db.get_rate_on_date(
            currency_in.curr_code, currency_in.on_date
        )
    except ValueError as e:
        errcode, errtxt = e.args[0]
        raise HTTPException(status_code=errcode, detail=errtxt)
    return {
        "success": True,
        "currency_code": currency_in.curr_code,
        "base_currency": db.date_updated.base_currency.code,
        "rate": db.rate,
        "last_updated": db.date_updated.created,
    }


@currencies_router.get(
    "/convert/{from_code}/{to_code}",
    response_model=resp.ConvertedResponse,
    responses=err.get_responses(err.all_errors),
)
async def convert_currency_rate(
    convert_in: req.ConvertIn = Depends(),
    currency_db: CurrencyDB = Depends(get_currency_db),
    auth_user: UserModel = Depends(get_current_active_user),
) -> Dict[str, Any]:

    try:
        converted: Dict[str, Any] = await currency_db.convert_rate(
            convert_in.from_code,
            convert_in.to_code,
            convert_in.amount,
            convert_in.on_date,
        )
    except ValueError as e:
        errcode, errtxt = e.args[0]
        raise HTTPException(status_code=errcode, detail=errtxt)

    return {
        "success": True,
        "from_currency_code": convert_in.from_code,
        "to_currency_code": convert_in.to_code,
        "amount": convert_in.amount,
        **converted,
    }


@currencies_router.get("/", response_model=resp.CurrenciesResponse)
async def get_all_currencies(
    currency_db: CurrencyDB = Depends(get_currency_db),
    auth_user: UserModel = Depends(get_current_active_user),
) -> Dict[str, Any]:

    currencies: List[str] = await currency_db.get_currency_codes()
    return {"success": True, "currencies": currencies}
