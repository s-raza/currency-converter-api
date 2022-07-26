from typing import Any, Dict

from .ext_api_interface import ExternalAPIBase, R


class ExchangeRateAPI(ExternalAPIBase):
    """
    Class to access currency rates from `Exchange Rate API <http://exchangerate.host>`_
    """

    def __init__(self, url: str = None):
        self._url = url

    @property
    def url(self) -> str:
        """
        URL for Exchange Rate API.

        :return: :obj:`str`
        """
        return self._url or "http://api.exchangerate.host/latest"

    @property
    def params(self) -> Dict[str, str]:
        """
        URL parameters for Exchange Rate API.

        :return: :obj:`str`
        """
        return {"base": "USD"}

    def formatted_rates(self, raw_rates: Any) -> R:
        """
        Get rates formatted as currency_code:rate from the Exchange Rate API.

        :param raw_rates: `dict` containing the currency:rate pairs from the
            Exchange Rate API.
        :type raw_rates: required

        :return:
            :obj:`dict`
            or
            :obj:`str`
        """
        return {"base_currency": raw_rates["base"], "rates": raw_rates["rates"]}
