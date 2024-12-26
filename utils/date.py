import datetime


def get_today_date() -> tuple[datetime.date, str]:
    """
    Get the current date YYYY-MM-DD and the day of the week
    """
    today = datetime.date.today()
    return today, today.strftime("%A")
