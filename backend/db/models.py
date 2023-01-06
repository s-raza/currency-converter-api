from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Currencies(Base):  # type: ignore
    """
    Currency codes

    :py:attr:`~Currencies.id`: Auto increment unique id

    :py:attr:`~Currencies.code`: Currency code

    :py:attr:`~Currencies.currency_update_dates`:
        Relational Object to :py:class:`CurrencyUpdateDates`

    :py:attr:`~Currencies.currency_updates`:
        Relational Object to :py:class:`CurrencyUpdates`

    """

    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(3), unique=True, index=True)
    currency_update_dates = relationship(
        "CurrencyUpdateDates", back_populates="base_currency"
    )
    currency_updates = relationship("CurrencyUpdates", back_populates="currency")

    def __repr__(self) -> str:
        return (
            f"Currencies[id: {self.id}, "
            f"code: {self.code}, "
            f"update_dates: {len(self.currency_update_dates)}, "
            f"currency_updates: {len(self.currency_updates)}]"
        )


class CurrencyUpdateDates(Base):  # type: ignore
    """
    Date on which a currency rate was saved along with the base rate.


    :py:attr:`~CurrencyUpdateDates.id`: Auto increment unique id

    :py:attr:`~CurrencyUpdateDates.created`:
        Date on which the update was saved

    :py:attr:`~CurrencyUpdateDates.base_currency_id`:
        Foreign Key to :py:class:`Currencies`
    :py:attr:`~CurrencyUpdateDates.base_currency`:
        Relational Object to :py:class:`Currencies`

    :py:attr:`~CurrencyUpdateDates.currency_updates`:
        Relational Object to :py:class:`CurrencyUpdates`

    """

    __tablename__ = "currency_update_dates"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created = Column(DATETIME(fsp=6), unique=True, index=True)
    base_currency_id = Column(Integer, ForeignKey("currencies.id"))
    base_currency = relationship("Currencies", back_populates="currency_update_dates")

    currency_updates = relationship("CurrencyUpdates", back_populates="date_updated")

    def __repr__(self) -> str:
        return (
            f"CurrencyUpdateDates[id: {self.id}, "
            f"created: {self.created}, "
            f"base_currency_id: {self.base_currency_id}, "
            f"currency_updates: {len(self.currency_updates)}]"
        )


class CurrencyUpdates(Base):  # type: ignore
    """
    Currency rate updates

    :py:attr:`~CurrencyUpdates.id`: Auto increment unique id

    :py:attr:`~CurrencyUpdates.currency_id`:
        Foreign Key to :py:class:`Currencies`
    :py:attr:`~CurrencyUpdates.currency`:
        Relational Object to :py:class:`Currencies`

    :py:attr:`~CurrencyUpdates.date_updated_id`:
        Foreign Key to :py:class:`CurrencyUpdateDates`
    :py:attr:`~CurrencyUpdates.date_updated`:
        Relational Object to :py:class:`CurrencyUpdateDates`

    :py:attr:`~CurrencyUpdates.rate`:
        Currency rate.
    """

    __tablename__ = "currency_updates"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    currency_id = Column(Integer, ForeignKey("currencies.id"))
    currency = relationship("Currencies", back_populates="currency_updates")

    date_updated_id = Column(Integer, ForeignKey("currency_update_dates.id"))
    date_updated = relationship(
        "CurrencyUpdateDates", back_populates="currency_updates"
    )
    rate = Column(Float(precision=32, decimal_return_scale=None))

    def __repr__(self) -> str:
        return (
            f"CurrencyUpdates[id: {self.id}, "
            f"currency_id: {self.currency_id}, "
            f"currency: {self.currency.code}, "
            f"date_updated_id: {self.date_updated_id}, "
            f"date_updated: {self.date_updated.created}, "
            f"rate: {self.rate}]"
        )


class User(Base):  # type: ignore
    """
    User model to implement authentication

    :py:attr:`~User.id`: Auto increment unique id

    :py:attr:`~User.username`: Username

    :py:attr:`~User.email`: Email

    :py:attr:`~User.full_name`: Full name

    :py:attr:`~User.full_name`: is the user disabled and not allowed to login

    :py:attr:`~User.password`: hashed password
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(65), unique=True, index=True, nullable=False)
    email = Column(String(65), unique=True, index=True)
    full_name = Column(String(65), index=True)
    disabled = Column(Boolean, default=False)
    password = Column(String(129), nullable=False)
