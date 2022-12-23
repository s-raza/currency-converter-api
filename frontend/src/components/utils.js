export function currencyFormatter(amount, currCode, format='en-US') {
    return (
        new Intl.NumberFormat(format, {
            style: 'currency',
            currency: currCode,
        }
        ).format(amount)
    )
}

export function convertCurrency(from_rate, base_rate, amount=1) {
    return (parseFloat(from_rate) / parseFloat(base_rate)) * parseFloat(amount)
}
