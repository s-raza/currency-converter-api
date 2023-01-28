API Endpoints Summary
=====================

#. ``GET``: **/currencies/rates/{curr_code}**

   Get the latest currency rate of the currency code ``curr_code``. If a parameter
   ``on_date`` is provided the last rate recorded on that particular date is returned.

   If ``on_date`` parameter is not provided, the absolute last rate recorded for the
   given currency code is returned for ``curr_code``

   The accepted date format is "%d-%m-%Y", any other format will result in a
   ``Bad Request`` response.

#. ``GET``: **/currencies/rates**

   Get the latest rates of all the currencies available. If a parameter ``on_date``
   is provided the last rate recorded on that particular date is returned for each
   currency

   If ``on_date`` parameter is not provided, the absolute last rates recorded for all
   the currency codes is returned.

   The accepted date format is "%d-%m-%Y", any other format will result in a
   ``Bad Request`` response.

#. ``GET``: **/currencies/convert/{from_code}/{to_code}**

   Convert the amount given in the ``amount`` query parameter from ``from_code`` currency
   code to ``to_code`` currency code.

   If a parameter ``on_date`` is provided the last rates recorded for the ``from_code``
   currency code and ``to_code`` on that particular date are used in the conversion calculation.

   If ``on_date`` parameter is not provided, the absolute last rates recorded for the
   ``from_code`` currency code and ``to_code`` are used in the conversion calculation.

   The accepted date format is "%d-%m-%Y", any other format will result in a
   ``Bad Request`` response.

#. ``GET``: **/currencies**

   Get a list of all the currencies available for conversion from the database.
