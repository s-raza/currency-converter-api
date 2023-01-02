export function currencyFormatter(amount, currCode, format='en-US') {
  return (
    new Intl.NumberFormat(format, {
      style: 'currency',
      currency: currCode,
    },
    ).format(amount)
  );
}

export function convertCurrency(fromRate, baseRate, amount=1) {
  return (parseFloat(fromRate) / parseFloat(baseRate)) * parseFloat(amount);
}
