import stripe


def find_or_create_vat():
    tax_rates = stripe.TaxRate.list()

    for tax_rate in tax_rates.auto_paging_iter():
        if tax_rate.percentage == 19.0:
            return tax_rate.id

    new_tax_rate = stripe.TaxRate.create(
        display_name="Mehrwertsteuer 19%",
        percentage=19.0,
        inclusive=True,
        country="DE",
    )

    return new_tax_rate.id
