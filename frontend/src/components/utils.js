export function currencyFormatter(amount, currCode, format='en-US') {
    return (
        new Intl.NumberFormat(format, {
            style: 'currency',
            currency: currCode,
        }
        ).format(amount)
    )
}
