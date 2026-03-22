import pandas as pd
import numpy as np
import datetime

from typing import Optional

from tomlkit.items import DateTime


def date_in_interval(date_time: str, date_beg: datetime, date_end: datetime):

    date = date_time.split(' ')[0]
    year = int(date.split('.')[2])
    month = int(date.split('.')[1])
    day = int(date.split('.')[0])

    curr_date = datetime.date(year, month, day)

    if date_beg <= curr_date <= date_end:
        return True
    else:
        return False


def spending_by_workday(transactions: pd.DataFrame,
                        inp_date: Optional[str] = None) -> pd.DataFrame:

    transactions['№'] = range(0, len(transactions))
    transactions.set_index('№', inplace=True, verify_integrity=True)

    last_transactions = []

    date = inp_date.split(' ')[0]

    if len(date) == 0:
        date = datetime.date

    if type(date) != datetime:
        year = int(date.split('-')[0])
        month = int(date.split('-')[1])
        day = int(date.split('-')[2])

        date = datetime.date(year, month, day)

    date_begin = date + datetime.timedelta(weeks=-8)

    transactions['in_interval'] = True

    for i in range(1,len(transactions)):
        tran = transactions.iloc[i]
        transactions.loc[i, 'in_interval'] = date_in_interval(tran['Дата операции'], date_begin, date)

    last_transactions = transactions.loc[transactions['in_interval'] == True]

    work_days = [0, 1, 2, 3, 4]
    weekend_days = [5, 6]

    # last_transactions['work_day'] = True

    for i in range(1, len(last_transactions)):
        tran = last_transactions.iloc[i]
        date_operation = tran['Дата операции']
        year_oper = int(date_operation.split(' ')[0].split('.')[2])
        month_oper = int(date_operation.split(' ')[0].split('.')[1])
        day_oper = int(date_operation.split(' ')[0].split('.')[0])

        date_op_date = datetime.date(year_oper, month_oper, day_oper)

        if int(date_op_date.weekday()) in work_days:
            last_transactions.loc[i, 'work_day'] = True
        else:
            last_transactions.loc[i, 'work_day'] = False

        if date_op_date.weekday() not in work_days and date_op_date.weekday() not in weekend_days:
            last_transactions.loc[i, 'work_day'] = False

    last_transactions = last_transactions.fillna(0)
    workday_grouped_trans = last_transactions.groupby('work_day').agg({'Сумма операции': 'mean'})

    # print(last_transactions[last_transactions['work_day'] == True])

    return workday_grouped_trans