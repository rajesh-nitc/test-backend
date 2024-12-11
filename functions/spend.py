from vertexai.generative_models import FunctionDeclaration

from utils.date import get_today_date

# Get today's date and day of the week
date, day_of_week = get_today_date()

# Define reusable templates for descriptions
date_info_template = f"""
Today's date is {date} ({day_of_week}).
Handle relative terms like "last year" or "this month" by calculating the appropriate start and end dates.

Examples:
- "How much did I spend on groceries this year?":
  Start Date: YYYY-01-01, End Date: today's date
- "What were my expenses in January?":
  Start Date: YYYY-01-01, End Date: YYYY-01-31
"""

category_description = """
Identify the spend category from user queries.

Examples:
- "What were my expenses this year?": null
- "How much did I spend on groceries this year?": groceries
"""

# Define the function declaration
get_spend_func = FunctionDeclaration(
    name="get_spend_func",
    description="Call this if the user is asking for spending information.",
    parameters={
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["groceries", "bills", "shopping", "travel", "entertainment"],
                "description": category_description,
                "nullable": True,
            },
            "start_date": {
                "type": "string",
                "description": date_info_template,
            },
            "end_date": {
                "type": "string",
                "description": date_info_template,
            },
        },
        "required": ["start_date", "end_date"],
    },
)
