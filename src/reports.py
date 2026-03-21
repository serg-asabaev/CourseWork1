import pandas as pd
import datetime

from typing import Optional

def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:

    if len(date) == 0:
        date = datetime.date


    return date