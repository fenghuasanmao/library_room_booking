from datetime import datetime


def date_later_or_early(second_date):
    date_now = datetime.now()
    now_year = date_now.year
    now_month = date_now.month
    now_day = date_now.day
    first_month = int(float(first_date.split("-")[1]))
    first_day = int(float(first_date.split("-")[2]))
    second_month = int(float(second_date.split("-")[1]))
    second_day = int(float(second_date.split("-")[2]))
    if second_month > first_month:
        return "later"
    elif second_month < first_month:
        return "early"
    elif second_day > first_day:
        return "later"
    elif second_day < first_day:
        return "early"
    else:
        return "same"


# print(date_later_or_early(date_now, "2022-03-10"))