import time
from typing import Any, Dict, Union

import requests  # type: ignore

from utils import logger

from .ext_api_interface import ExternalAPIBase, R

download_logger = logger.get_logger(__name__)


class CurrencyRatesDownloader:
    """
    Generic downloader that accepts an instance of object
    based on :obj:`ExternalAPIBase`.

    Retries retrieval of currency rates from the external API source upon failure,
    with configurable options to retrying.

    :param ext_api: :obj:`ExternalAPIBase`
    :type ext_api: required

    :param max_retries: Maximum number of retrial attempts, `default=5`
    :type max_retries: optional

    :param time_out: Initial time out for retrials in seconds, each time a failure
        occurs, this is incremented by `increment_timeout`, `default=5` seconds.
    :type time_out: optional

    :param increment_timeout: Number of seconds to increment for each subsequent
        attempt, `default=5` seconds
    :type increment_timeout: optional

    """

    def __init__(
        self,
        ext_api: ExternalAPIBase,
        max_retries: int = 5,
        time_out: int = 5,
        increment_timeout: int = 5,
    ):

        self.api = ext_api

        self.max_retries = max_retries
        self.time_out = time_out
        self.increment_timeout = increment_timeout

        # Set User-Agent header to evade being flagged as an automated scraper.
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0)"
            "Gecko/20100101 Firefox/102.0"
        )
        self.headers: Dict[str, str] = {"User-Agent": self.user_agent}

    def add_headers(self, headers: Dict[str, Any]) -> None:
        """
        Add additional headers before sending request to the external API, if required.

        :param headers: `dict` of header key:value pairs
        :type headers: required

        :return: `None`
        """

        for k, v in headers.items():
            self.headers[k] = v

    def get_rates(self) -> Union[R, None]:
        """
        Get rates from the external source API for currency rates.

        :return: `dict` containing the currency:rate pairs from the
            external source API for currency rates.
        """

        success = False

        while not success and self.max_retries > 0:
            try:
                req_result = requests.get(
                    self.api.url, headers=self.headers, params=self.api.params
                )
                success = True
            except Exception as e:
                download_logger.error(
                    f"Error retrieving rates from: {self.api.url}\n\n"
                    f"Error: {e.args}\n\n"
                    f"Retrying in: {self.time_out}s"
                    f", attempts left: {self.max_retries}"
                )
                time.sleep(self.time_out)
                self.max_retries -= 1
                self.time_out += self.increment_timeout
                continue

        if success is True:
            return self.api.formatted_rates(req_result.json())
        else:
            return None
