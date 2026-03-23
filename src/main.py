import pandas as pd

from reports import spending_by_workday
from services import physical_transactions
from tests.conftest import afternoon_greeting
from views import greetings

if __name__ == "__main__":

    my_date = "2020-03-11 20:51:36"

    print(greetings(my_date))

    print(physical_transactions())
    print(afternoon_greeting)

    df = pd.read_excel("../data/operations.xlsx")
    result = df.to_dict(
        orient="records",
    )
    df1 = spending_by_workday(df, my_date)

    frame_dict = df1.to_dict()

    print(frame_dict)
