from vertexai.generative_models import FunctionDeclaration

from utils.date import get_today_date

# Get today's date and day of the week
date, day_of_week = get_today_date()

DESCRIPTIONS = {
    "date": f"""
Identify the date from user queries.
Today's date is {date} ({day_of_week}).
Handle relative terms like "last year" or "this month" by calculating the appropriate start and end dates.

Examples:
- "How much did I spend on groceries this year?":
  Start Date: YYYY-01-01, End Date: today's date
- "What were my expenses in January?":
  Start Date: YYYY-01-01, End Date: YYYY-01-31
- "spend last year":
  Start Date: YYYY-01-01, End Date: YYYY-12-31
    """,
    "category": """
Identify the spend category from user queries.
Examples:
- "What were my expenses this year?": null
- "How much did I spend on groceries this year?": groceries
    """,
}

# Define the function declaration
get_spend_func = FunctionDeclaration(
    name="get_spend_func",
    description="Call this function for user queries about expenses, spending, or financial information.",
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
                "description": DESCRIPTIONS["date"],
            },
            "end_date": {
                "type": "string",
                "description": DESCRIPTIONS["date"],
            },
        },
        "required": ["start_date", "end_date"],
    },
)
