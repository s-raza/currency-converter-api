from abc import ABC, abstractmethod
from typing import Any, Dict, Union

R = Dict[str, Any]


class ExternalAPIBase(ABC):
    """
    Base class for implementing an external API source for currency rates.
    """

    @property
    @abstractmethod
    def url(self) -> str:
        """
        URL for the external API source for currency rates.

        :return: :obj:`str`
        """
        ...

    @property
    @abstractmethod
    def params(self) -> Dict[str, str]:
        """
        URL parameters for the external API source for currency rates.

        :return: :obj:`str`
        """
        ...

    @abstractmethod
    def formatted_rates(self, raw_rates: Union[Dict[str, str], str]) -> R:
        """
        Get rates formatted as currency_code:rate from the external source API for
        currency rates.

        :param raw_rates: Dictionary containing the currency:rate pairs or a string,
             depending on the API source for currency rates.
        :type raw_rates: required

        :return:
            :obj:`dict`
            or
            :obj:`str`
        """
        ...
