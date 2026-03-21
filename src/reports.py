import pandas as pd
import datetime

from typing import Optional


def date_in_interval(date_time: str, date_beg: datetime, date_end: datetime):

    date = date_time.split(' ')[0]
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])

    curr_date = datetime.date(year, month, day)

    if date_beg <= curr_date <= date_end:
        return True
    else:
        return False


def spending_by_workday(transactions: pd.DataFrame,
                        inp_date: Optional[str] = None) -> pd.DataFrame:

    date = inp_date.split(' ')[0]

    if len(date) == 0:
        date = datetime.date

    if type(date) != datetime:
        year = int(date.split('-')[0])
        month = int(date.split('-')[1])
        day = int(date.split('-')[2])

        date = datetime.date(year, month, day)

    date_begin = date + datetime.timedelta(weeks=-8)

    transactions['in_interval'] = date_in_interval(transactions[]['Дата операции'], date_begin, date)

    for i in transactions:


    work_days = [0, 1, 2, 3, 4]
    weekend_days = [5, 6]


    return transactions # last_transactions