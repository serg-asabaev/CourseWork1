import pytest
import pandas as pd
import datetime


from src.reports import spending_by_workday


def test_spending_by_workday(mean_spending):
    my_date = '2020-03-11 20:51:36'
    df = pd.read_excel('../data/operations.xlsx')
    assert spending_by_workday(df, my_date).to_dict() == mean_spending


def test_spending_by_workday_empty_date(empty_spending):
    my_date = str(datetime.datetime.now())
    df = pd.read_excel('../data/operations.xlsx')
    print(my_date.split('.')[0])
    assert spending_by_workday(df, my_date.split('.')[0]).to_dict() == empty_spending