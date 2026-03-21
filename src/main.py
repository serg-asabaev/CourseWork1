import pandas as pd

from views import greetings
from services import physical_transactions
from reports import spending_by_workday
from external_api import get_actual_currency_rate

if __name__ == '__main__':

    my_date = '2020-03-11 20:51:36'

    # print(greetings(my_date))

    # print(physical_transactions())

    # df = pd.read_excel('../data/operations.xlsx', index_col=0)
    # result = df.to_dict(orient="records")
    # print(spending_by_workday(df, my_date))
    #https://pypi.org/project/yfinance/

    print(get_actual_currency_rate())