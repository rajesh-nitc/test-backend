from vertexai.generative_models import FunctionDeclaration

from utils.date import get_today_date
from utils.text import dedent_and_strip

# Get today's date and day of the week
date, day_of_week = get_today_date()

DESCRIPTIONS = {
    "FUNCTION": dedent_and_strip(
        f"""
Handle user queries about expenses, spending, or financial information.
Extract the category, start_date, and end_date from user queries.
Today's date is {date} ({day_of_week}). Handle relative terms like "last year" or "this month" by calculating the appropriate start and end dates.
Example usage:
    - What were my expenses this year?: category is null, start_date is YYYY-01-01, end_date is today's date
    - How much did I spend on groceries last year?: category is groceries, start_date is YYYY-01-01, end_date is YYYY-12-31
    - What were my expenses in January?: category is null, start_date is YYYY-01-01, end_date is YYYY-01-31
    - spend: clarify the query as you don't have enough information
"""
    ),
    "start_date": dedent_and_strip(
        """
Start date for the expenses query
"""
    ),
    "end_date": dedent_and_strip(
        """
End date for the expenses query
"""
    ),
    "category": dedent_and_strip(
        """
Category of the expenses query
"""
    ),
}

# Define the function declaration
get_spend_func = FunctionDeclaration(
    name="get_spend_func",
    description=DESCRIPTIONS["FUNCTION"],
    parameters={
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["groceries", "bills", "shopping", "travel", "entertainment"],
                "description": DESCRIPTIONS["category"],
                "nullable": True,
            },
            "start_date": {
                "type": "string",
                "description": DESCRIPTIONS["start_date"],
            },
            "end_date": {
                "type": "string",
                "description": DESCRIPTIONS["end_date"],
            },
        },
        "required": ["start_date", "end_date"],
    },
)
