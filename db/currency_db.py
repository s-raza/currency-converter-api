import datetime
from typing import Any, Dict, List, Union

from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from .models import Currencies, CurrencyUpdateDates, CurrencyUpdates, User


class CurrencyDB:
    """
    Interface to the Currency Database.

    :param session: SQLAlchemy :obj:`Session` object.
    :type session: required

    """

    def __init__(self, session: Session) -> None:

        self.session = session

    def get_pwd_hash(self, plain: str) -> str:
        """
        Get hashed password from plain text

        :param plain: Plain text
        :type plain: required

        :return: :obj:`str` hashed password

        """
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(plain)

    async def get_user(self, username: str) -> Union[User, None]:
        """
        Get User object from DB

        :param username: Username
        :type username: required

        :return:
            :obj:`User` if found

            :obj:`None` if not found

        """
        result = await self.session.execute(select(User).filter_by(username=username))
        return result.scalars().first()

    async def add_user(
        self,
        username: str,
        password: str,
        email: str = None,
        full_name: str = None,
        disabled: bool = False,
    ) -> None:

        """
        Add user to DB

        :param username: Username
        :type username: required

        :param password: Password
        :type password: required

        :param email: Email
        :type email: optional

        :param full_name: Full name
        :type full_name: optional

        :param disabled: If the user is to be added as disabled
            :obj:`True` or :obj:`False`
        :type disabled: optional

        :return:
            :obj:`User` if found

            :obj:`None` if not found

        """

        user = User(
            username=username,
            email=email,
            full_name=full_name,
            disabled=disabled,
            password=self.get_pwd_hash(password),
        )

        self.session.add(user)
        await self.session.commit()

    @property
    async def last_update_date(self) -> CurrencyUpdateDates:
        """
        Get the DB object corresponding to the last update from external currency API.

        :return: :obj:`db.models.CurrencyUpdateDates`
        """

        q = select(CurrencyUpdateDates).order_by(CurrencyUpdateDates.id.desc()).limit(1)

        result = await self.session.execute(q)
        result = result.scalars().first()

        return result

    async def __add_currency(self, curr_code: str) -> Currencies:
        """
        Private method to add a new currency.

        :param curr_code: Currency code to add.
        :type curr_code: required

        :return: :obj:`db.models.Currencies`
        """

        curr = Currencies(code=curr_code)
        self.session.add(curr)
        await self.session.flush()

        return curr

    async def get_or_create(self, curr_code: str) -> Currencies:
        """
        Get currency object, create it if it does not exist.

        :param curr_code: Currency code.
        :type curr_code: required

        :return: :obj:`db.models.Currencies`
        """

        q = select(Currencies).filter_by(code=curr_code)
        result = await self.session.execute(q)
        curr = result.scalars().first()

        if curr is None:
            return await self.__add_currency(curr_code=curr_code)

        return curr

    async def get_currency(self, curr_code: str) -> Currencies:
        """
        Get currency object, raise error if it does not exist.

        :param curr_code: Currency code.
        :type curr_code: required

        :raises ValueError: If currency code not found in database.

        :return: :obj:`db.models.Currencies`
        """

        q = select(Currencies).filter_by(code=curr_code)
        result = await self.session.execute(q)
        curr = result.scalars().first()

        if curr is None:
            raise ValueError((404, f"Currency code {curr_code} does not exist"))

        return curr

    async def add_update(
        self, base_curr: str, update: Dict[str, float], for_date: str = None
    ) -> None:
        """
        Add a currency update to DB.

        :param base_curr: Base currency of the update.
        :type base_curr: required

        :param update: Dictionary of currency_code:rate pairs.
        :type update: required

        :param for_date:
            Particular date to record the update against, in the "%d-%m-%Y" format,
            particularly useful in tests.
            If no date is provided, the current date is used.
        :type for_date: optional

        :raises ValueError: If the date is not in the "%d-%m-%Y" format.

        :return: :obj:`None`
        """

        try:
            if for_date is None:
                for_date_obj = datetime.datetime.utcnow()
            else:
                date_part = datetime.datetime.strptime(for_date, "%d-%m-%Y")
                time_part = datetime.datetime.utcnow().time()
                for_date_obj = datetime.datetime.combine(date_part, time_part)
        except ValueError:
            raise ValueError("Malformed date format, expected DD-MM-YYYY")

        base_curr_obj = await self.get_or_create(base_curr)

        curr_update_date_obj = CurrencyUpdateDates(
            created=for_date_obj, base_currency=base_curr_obj
        )

        for code, rate in update.items():
            curr_update_date_obj.currency_updates.append(
                CurrencyUpdates(currency=await self.get_or_create(code), rate=rate)
            )

        self.session.add(curr_update_date_obj)
        await self.session.commit()

    async def get_currency_codes(self) -> List[str]:
        """
        Get a list of all the currency codes available in the DB.

        :return: :obj:`list`
        """

        q = select(Currencies)
        result = await self.session.execute(q)
        result = result.scalars().all()

        return [curr.code for curr in result]

    async def get_currency_rates(self, on_date: str = None) -> Dict[str, Any]:
        """
        Get last rates updated in DB for all currency codes.

        If a date is not provided, the date from the last update is used.

        :param on_date:
            Particular date for which to get the rate, in the "%d-%m-%Y" format
        :type on_date: optional

        :raises ValueError: If the date is not in the "%d-%m-%Y" format.

        :raises ValueError: If an empty result is returned from the query.

        :return:
            :obj:`Dict[created_date: date, base_currency: currency_code,
            rates: Dict[currency_code: rate]]`
            if the query returns a result else raises ValueError

        """

        last_update_date = await self.last_update_date

        if on_date is not None:
            try:
                date_obj = datetime.datetime.strptime(on_date, "%d-%m-%Y")
            except ValueError:
                raise ValueError((400, "Malformed date format, expected DD-MM-YYYY"))
        else:
            date_obj = last_update_date.created

        q = (
            select([CurrencyUpdates, Currencies, CurrencyUpdateDates])
            .where(Currencies.id == CurrencyUpdates.currency_id)
            .where(CurrencyUpdates.date_updated_id == CurrencyUpdateDates.id)
            .options(selectinload(CurrencyUpdateDates.base_currency))
            .where(func.DATE(CurrencyUpdateDates.created) == date_obj.date())
            .order_by(CurrencyUpdateDates.id.asc())
            .options(selectinload(CurrencyUpdates.date_updated))
        )

        result = await self.session.execute(q)
        result = result.scalars()
        rates = {item.currency.code: item.rate for item in result}

        if rates:
            return {
                "created": date_obj,
                "base_currency": last_update_date.base_currency.code,
                "rates": rates,
            }
        else:
            date_str = datetime.datetime.strftime(date_obj, "%d-%m-%Y")
            raise ValueError((404, f"No entry for date {date_str} exists"))

    async def get_rate_on_date(
        self, curr_code: str, on_date: str = None
    ) -> CurrencyUpdates:
        """
        Get last rate updated in DB for a particular date and currency code.

        If a date is not provided, the date from the last update is used.

        :param curr_code: Currency code.
        :type curr_code: required

        :param on_date:
            Particular date for which to get the rate, in the "%d-%m-%Y" format
        :type on_date: optional

        :raises ValueError: If the date is not in the "%d-%m-%Y" format.

        :raises ValueError: If an empty result is returned from the query.

        :return:
            :obj:`CurrencyUpdates` if the query returns a result else raises ValueError

        """

        try:
            curr_obj = await self.get_currency(curr_code)
        except ValueError as e:
            raise ValueError(e.args[0])

        if on_date is not None:
            try:
                date_obj = datetime.datetime.strptime(on_date, "%d-%m-%Y")
            except ValueError:
                raise ValueError((400, "Malformed date format, expected DD-MM-YYYY"))
        else:
            last_update_date = await self.last_update_date
            date_obj = last_update_date.created

        q = (
            select([CurrencyUpdates, Currencies, CurrencyUpdateDates])
            .where(Currencies.code == curr_obj.code)
            .where(Currencies.id == CurrencyUpdates.currency_id)
            .where(CurrencyUpdates.date_updated_id == CurrencyUpdateDates.id)
            .options(selectinload(CurrencyUpdateDates.base_currency))
            .where(func.DATE(CurrencyUpdateDates.created) == date_obj.date())
            .order_by(CurrencyUpdateDates.id.desc())
            .options(selectinload(CurrencyUpdates.date_updated))
            .limit(1)
        )

        result = await self.session.execute(q)
        result = result.scalars().first()

        if result is not None:
            return result
        else:
            date_str = datetime.datetime.strftime(date_obj, "%d-%m-%Y")
            raise ValueError((404, f"No entry for date {date_str} exists"))

    async def convert_rate(
        self, from_curr_code: str, to_curr_code: str, amount: float, on_date: str = None
    ) -> Dict[str, Any]:
        """
        Convert currency from one to another based on the rate on the given date.

        If a date is not provided, the date from the last update is used.


        :param from_curr_code: Currency code to convert from.
        :type from_curr_code: required

        :param to_curr_code: Currency code to convert to.
        :type to_curr_code: required

        :param amount: Amount to be converted
        :type amount: required

        :param on_date: Currency rates from this date will be used if provided.
        :type on_date: optional

        :raises ValueError: Propogated from exception stack

        :return:
            :obj:`dict` of Currency rate converted from -> to, base currency
            and last updated date of the currency from the external API
        """
        try:
            from_curr_obj = await self.get_currency(from_curr_code)
            to_curr_obj = await self.get_currency(to_curr_code)

            from_curr_update_obj: CurrencyUpdates = await self.get_rate_on_date(
                from_curr_obj.code, on_date
            )

            to_curr_update_obj: CurrencyUpdates = await self.get_rate_on_date(
                to_curr_obj.code, on_date
            )

            last_updated = from_curr_update_obj.date_updated.created
            base_currency = to_curr_update_obj.date_updated.base_currency.code
            converted = (to_curr_update_obj.rate / from_curr_update_obj.rate) * amount
        except ValueError as e:
            raise ValueError(e.args[0])

        return {
            "converted": converted,
            "base_currency": base_currency,
            "last_updated": last_updated,
        }
