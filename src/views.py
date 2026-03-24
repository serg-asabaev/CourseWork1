

from src.external_api import get_action_prices, get_actual_currency_rate
from src.read_files import read_excel


def card_info(excel_data: list[dict], year: int, month: int, day: int):
    """Получение информации по картам"""

    operations_info = []
    cards = []

    for record in excel_data:
        record_date_str = record["Дата платежа"]

        if type(record_date_str) is not str:
            record_date_str = "01.01.1900"

        if (
            year == int(record_date_str.split(".")[2])
            and month == int(record_date_str.split(".")[1])
            and day >= int(record_date_str.split(".")[0])
        ):

            last_digits = record["Номер карты"]

            if type(record["Номер карты"]) is not str:
                last_digits = "*"

            last_digits = last_digits.replace("*", "")
            operation_sum = record["Сумма операции"]
            cashback = record["Кэшбэк"]

            if str(cashback) == "nan":
                cashback = 0

            operation_info = {
                "last_digits": last_digits,
                "sum": operation_sum,
                "cashback": cashback,
            }

            operations_info.append(operation_info)

    card_numbers = []
    card_sums = []
    card_cashbacks = []

    for operation in operations_info:
        if (
            operation["last_digits"] not in card_numbers
            and operation["last_digits"] != ""
        ):
            card_numbers.append(operation["last_digits"])
            card_sums.append(0)
            card_cashbacks.append(0)
        elif operation["last_digits"] != "":
            index = card_numbers.index(operation["last_digits"])
            card_sums[index] -= float(operation["sum"])
            card_cashbacks[index] += float(operation["cashback"])

    for card_num in card_numbers:
        index = card_numbers.index(card_num)

        card = {
            "last_digits": card_numbers[index],
            "total_spent": card_sums[index],
            "cashback": card_cashbacks[index],
        }

        cards.append(card)

    return cards


def get_top_five_operations(excel_data: list[dict], year: int, month: int, day: int):
    """Получение топ-5 транзакций по сумме платежа"""

    monthly_data = []
    top_five = []

    for record in excel_data:
        record_date_str = record["Дата платежа"]

        if type(record_date_str) is not str:
            record_date_str = "01.01.1900"

        if (
            year == int(record_date_str.split(".")[2])
            and month == int(record_date_str.split(".")[1])
            and day >= int(record_date_str.split(".")[0])
        ):
            monthly_data.append(record)

    sorted_list = sorted(monthly_data, key=lambda x: x["Сумма операции"], reverse=False)

    ind = 0

    for list_item in sorted_list:

        date = list_item["Дата платежа"]
        amount = list_item["Сумма операции"]
        category = list_item["Категория"]
        description = list_item["Описание"]

        res_dict = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        top_five.append(res_dict)

        if ind > 5:
            break
        ind += 1

    return top_five


def greetings(date_time: str):
    """Функция приветствия. В качестве результата выдает строку приветствия на основе времени"""

    date = date_time.split(" ")[0]
    time = date_time.split(" ")[1]

    date_list = date.split("-")
    time_list = time.split(":")

    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])

    hours = int(time_list[0])

    if 5 < hours < 10:
        greeting_str = "Доброе утро"
    elif 10 < hours < 17:
        greeting_str = "Добрый день"
    elif 17 < hours < 22:
        greeting_str = "Добрый вечер"
    else:
        greeting_str = "Доброй ночи"

    result = {"greeting": greeting_str}

    excel_data = read_excel("../data/operations.xlsx")

    # df = pd.read_excel('../data/operations.xlsx', index_col=0)
    # excel_data = df.to_dict(orient="records")

    cards = card_info(excel_data, year, month, day)
    result["cards"] = cards

    top_transactions = get_top_five_operations(excel_data, year, month, day)
    result["top_transactions"] = top_transactions

    result["currency_rates"] = get_actual_currency_rate()
    result["stock_prices"] = get_action_prices(date_time)

    return result
