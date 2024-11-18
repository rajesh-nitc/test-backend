from vertexai.generative_models import FunctionDeclaration

from utils.date import get_today_date

date, day_of_week = get_today_date()

get_spend_func = FunctionDeclaration(
    name="get_spend_func",
    description="Call this if user is asking for the spend",
    parameters={
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["groceries", "bills", "shopping", "travel", "entertainment"],
                "description": """
                You are an AI assistant trained to extract spend category information from user queries. for e.g. groceries, bills, shopping, travel, entertainment
                If the user asks, What were my expenses in January?, it means the user is looking for total spend across all spend categories
                If the user asks, What were my expenses this year?, it means the user is looking for total spend across all spend categories
                If the user asks, How much did I spend on groceries this year?, extract groceries from the query

                Return the extracted information in the format:
                shopping
                null
                """,
                "nullable": True,
            },
            "start_date": {
                "type": "string",
                "description": f"""
                You are an AI assistant trained to extract date-related information from user queries. The user will provide queries, and your task is to identify and extract any date in the query, including relative terms like "last year" or "this month"
                This is today's date {date} ({day_of_week}) in the format YYYY-MM-DD
                If the user asks, How much did I spend on groceries this year?, extract the start of year from the today's date
                If the user asks, What were my expenses in January?, extract the start of month January and year from today's date

                Return the extracted information in the format:
                YYYY-01-01
                YYYY-01-01
                """,
            },
            "end_date": {
                "type": "string",
                "description": f"""
                You are an AI assistant trained to extract date-related information from user queries. The user will provide queries, and your task is to identify and extract any date in the query, including relative terms like "last year" or "this month"
                This is today's date {date} ({day_of_week}) in the format YYYY-MM-DD
                If the user asks, How much did I spend on groceries this year?, extract the end date which is today's date
                If the user asks, What were my expenses in January?, extract the end date of January and year from today's date

                Return the extracted information in the format:
                YYYY-MM-DD
                YYYY-01-31
                """,
            },
        },
        "required": ["start_date", "end_date"],
    },
)
