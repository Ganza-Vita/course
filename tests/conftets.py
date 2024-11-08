import json

import pandas as pd
import pytest


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": ["Супермаркеты",
                                       "Одежда",
                                       "Рестораны",
                                       "Супермаркеты",
                                       "Супермаркеты",
                                       "Супермаркеты"],
                         "Дата операции": ["31.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "29.11.2021 16:44:00",
                                           "27.07.2024 16:44:00"],
                         "Сумма операции": [-1,
                                            -2,
                                            -3,
                                            -4,
                                            -5,
                                            -6],
                         "Кэшбэк": [10, 20, 0, 30, 40, 50],
                         "Номер карты": ["*1111", "*1111", "*2222", "*2222", "*3333", "*3333"],
                         "Описание": ["Операция 1", "Операция 2", "Операция 3",
                                      "Операция 4", "Операция 5", "Операция 6"]},
                        index=[0, 1, 2, 3, 4, 5])

    return data


@pytest.fixture
def res_spending_by_category() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": ["Супермаркеты", "Супермаркеты"],
                         "Дата операции": ["31.12.2021 16:44:00", "30.12.2021 16:44:00"],
                         "Сумма операции": [-1, -4],
                         "Кэшбэк": [10, 30],
                         "Номер карты": ["*1111", "*2222"],
                         "Описание": ["Операция 1", "Операция 4"]},
                        index=[0, 3])
    return data


@pytest.fixture
def res_spending_by_category_without_date() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": ["Супермаркеты"],
                         "Дата операции": ["27.07.2024 16:44:00"],
                         "Сумма операции": [-6],
                         "Кэшбэк": [50],
                         "Номер карты": ["*3333"],
                         "Описание": ["Операция 6"]},
                        index=[5])
    return data


@pytest.fixture()
def cashback_12() -> str:
    data = """{"Супермаркеты": 40, "Одежда": 20}"""
    return data


@pytest.fixture()
def res_get_data_filter_by_date() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": ["Супермаркеты",
                                       "Одежда",
                                       "Рестораны",
                                       "Супермаркеты"],
                         "Дата операции": ["31.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "30.12.2021 16:44:00"],
                         "Сумма операции": [-1,
                                            -2,
                                            -3,
                                            -4],
                         "Кэшбэк": [10, 20, 0, 30],
                         "Номер карты": ["*1111", "*1111", "*2222", "*2222"],
                         "Описание": ["Операция 1", "Операция 2", "Операция 3", "Операция 4"]},
                        index=[0, 1, 2, 3])

    return data


@pytest.fixture()
def top_transactions() -> list[dict]:
    data = [{"date": "27.07.2024 16:44:00", "amount": -6, "category": "Супермаркеты", "description": "Операция 6"},
            {"date": "29.11.2021 16:44:00", "amount": -5, "category": "Супермаркеты", "description": "Операция 5"},
            {"date": "30.12.2021 16:44:00", "amount": -4, "category": "Супермаркеты", "description": "Операция 4"},
            {"date": "30.12.2021 16:44:00", "amount": -3, "category": "Рестораны", "description": "Операция 3"},
            {"date": "30.12.2021 16:44:00", "amount": -2, "category": "Одежда", "description": "Операция 2"}]
    return data


@pytest.fixture()
def res_main() -> str:
    top = [{"date": "30.12.2021 16:44:00", "amount": -4, "category": "Супермаркеты", "description": "Операция 4"},
           {"date": "30.12.2021 16:44:00", "amount": -3, "category": "Рестораны", "description": "Операция 3"},
           {"date": "30.12.2021 16:44:00", "amount": -2, "category": "Одежда", "description": "Операция 2"},
           {"date": "31.12.2021 16:44:00", "amount": -1, "category": "Супермаркеты", "description": "Операция 1"}]
    cards = [{"last_digits": "1111", "total_spent": 3, "cashback": 30},
             {"last_digits": "2222", "total_spent": 7, "cashback": 30}]
    data = {"greeting": "Добрый день",
            "cards": cards,
            "top_transactions": top,
            "currency_rates": [{'currency': 'USER', 'rate': 100}],
            "stock_prices": [{'stock': 'USER', 'price': 100}]}
    result = json.dumps(data, ensure_ascii=False)
    return result