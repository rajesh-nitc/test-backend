from typing import Literal

from functions.api.docstrings import spend


def get_spend_func(
    start_date: str,
    end_date: str,
    category: (
        Literal["groceries", "bills", "shopping", "travel", "entertainment"] | None
    ) = None,
):
    return {"start_date": start_date, "end_date": end_date, "category": category}


get_spend_func.__doc__ = spend
