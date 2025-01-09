from typing import Literal

from functions.search.docstrings import toys


def search_toys_func(
    query: str,
    top_k: int | None = None,
    operator: (
        Literal["LESS", "LESS_EQUAL", "EQUAL", "GREATER_EQUAL", "GREATER"] | None
    ) = None,
    price: float | None = None,
):
    return {"query": query, "top_k": top_k, "operator": operator, "price": price}


search_toys_func.__doc__ = toys
