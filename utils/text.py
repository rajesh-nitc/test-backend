from textwrap import dedent


def dedent_and_strip(text: str) -> str:
    """Cleans text by applying dedent and strip."""
    return dedent(text).strip()
