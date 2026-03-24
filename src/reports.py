import datetime
from typing import Optional

import pandas as pd


def date_in_interval(date_time: str, date_beg: datetime, date_end: datetime):
    """Фильтрует датафрейм по переданной дате. Берет последние 3 месяца"""

    date = date_time.split(" ")[0]
    year = int(date.split(".")[2])
    month = int(date.split(".")[1])
    day = int(date.split(".")[0])

    curr_date = datetime.date(year, month, day)

    if date_beg <= curr_date <= date_end:
        return True
    else:
        return False


def is_workday(date: str, work_days: list, weekend_days: list):
    """Проверяет рабочий или выходной день передан на вход."""

    year_oper = int(date.split(" ")[0].split(".")[2])
    month_oper = int(date.split(" ")[0].split(".")[1])
    day_oper = int(date.split(" ")[0].split(".")[0])

    date_op_date = datetime.date(year_oper, month_oper, day_oper)

    if int(date_op_date.weekday()) in work_days:
        return "Рабочий"
    else:
        return "Выходной"


def spending_by_workday(
    transactions: pd.DataFrame, inp_date: Optional[str] = None
) -> pd.DataFrame:
    """Выводит средние траты в рабочий и в выходной день за последние три месяца(от переданной даты)"""

    transactions["№"] = range(0, len(transactions))
    transactions.set_index("№", inplace=True, verify_integrity=True)

    date = inp_date.split(" ")[0]

    if len(date) == 0:
        date = datetime.date

    if type(date) is not datetime:
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2])

        date = datetime.date(year, month, day)

    date_begin = date + datetime.timedelta(weeks=-12)

    transactions["in_interval"] = True

    for i in range(1, len(transactions)):
        tran = transactions.iloc[i]
        transactions.loc[i, "in_interval"] = date_in_interval(
            tran["Дата операции"], date_begin, date
        )

    last_transactions = transactions.loc[transactions["in_interval"] == True]

    last_transactions["№"] = range(0, len(last_transactions))
    last_transactions.set_index("№", inplace=True, verify_integrity=True)

    work_days = [0, 1, 2, 3, 4]
    weekend_days = [5, 6]

    last_transactions["work_day"] = "Рабочий"

    for i in range(1, len(last_transactions)):
        tran = last_transactions.iloc[i]
        date_operation = tran["Дата операции"]
        last_transactions.loc[i, "work_day"] = is_workday(
            date_operation, work_days, weekend_days
        )

    workday_grouped_trans = last_transactions.groupby("work_day").agg(
        {"Сумма операции": "mean"}
    )

    return workday_grouped_trans
