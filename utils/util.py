import locale


def error_detail(variables: list[str], msgs: list[str]):
    return {"loc": variables, "msg": msgs, "type": "value_error"}


def format_currency(value: float) -> str:
    # Set the locale to Brazilian Portuguese
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # Format the value as currency
    formatted_value = locale.currency(value, grouping=True)

    # Return the formatted value
    return formatted_value
