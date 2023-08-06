__all__ = ["format_number"]

from datetime import datetime


def format_date_month(date: datetime) -> str:
    return date.strftime("%d/%m")


def format_number(value: float | int, *, format_spec=".1f", parenthesized_negative=True) -> str:
    def format_value(value: float | int) -> str:
        return format(value, format_spec)

    if parenthesized_negative and value < 0:
        value_str = format_value(abs(value))
        return f"({value_str})"
    return format_value(value)
