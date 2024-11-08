import datetime
import json
import logging
import math
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

utils_logger = logging.getLogger(__name__)
utils_file_formater = logging.Formatter(
    "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
    "%d.%m.%Y %H:%M:%S"
)

# Убедитесь, что директория для логов существует
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)  # Создаёт директорию, если её нет

utils_file_handler = logging.FileHandler(os.path.join(log_directory, "project.log"), "a")
utils_file_handler.setFormatter(utils_file_formater)
utils_logger.setLevel(logging.DEBUG)
utils_logger.addHandler(utils_file_handler)

load_dotenv(".env")


def greetings(end_date: datetime.datetime) -> str:
    """
    Функция определяет время суток
    """
    utils_logger.info("Начало работы функции greetings")
    if 0 <= end_date.hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= end_date.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= end_date.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    utils_logger.info("Конец работы функции greetings")
    return greeting


def get_data_filter_by_date(file_name: str, end_date: datetime.datetime) -> pd.DataFrame:
    """
    Считывание данных и фильтрация по дате
    """
    utils_logger.info("Начало работы функции get_data_filter_by_date")

    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)
    operations = pd.read_excel(os.path.join("data/", file_name))
    df_date = pd.to_datetime(operations["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    operations = operations[(start_date <= df_date) & (df_date <= end_date)]

    utils_logger.info("Конец работы функции get_data_filter_by_date")
    return operations


def get_cards_info(operations: pd.DataFrame) -> list[dict]:
    """
    Получение информации по картам (последние 4 цифры, общая сумма расходов, кешбэк)
    """
    utils_logger.info("Начало работы функции get_cards_info")

    expenses = operations[operations["Сумма операции"] < 0]
    expenses_group_cards = expenses.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"})

    fieldnames = ["last_digits", "total_spent", "cashback"]
    card_numbers = expenses_group_cards.index.tolist()
    cards_list = []
    card_dict = {}
    counter = 0
    for row in expenses_group_cards.iterrows():
        card_dict[fieldnames[0]] = card_numbers[counter][-4:]
        for i, element in enumerate(row[1], 1):
            card_dict[fieldnames[i]] = element
        cards_list.append(card_dict.copy())
        counter += 1

    for card in cards_list:
        card["total_spent"] *= -1
        card["total_spent"] = round(card["total_spent"], 2)

    utils_logger.info("Конец работы функции get_cards_info")
    return cards_list


def get_top_transactions(operations: pd.DataFrame) -> list[dict]:
    """
    Топ 5 по сумме платежа
    """
    utils_logger.info("Начало работы функции get_top_transactions")

    operations_with_fabs = operations
    operations_with_fabs["Сумма операции по модулю"] = operations["Сумма операции"].apply(math.fabs)
    sorted_operations_by_amount = operations_with_fabs.sort_values(by="Сумма операции по модулю", ascending=False)
    fieldnames = ["date", "amount", "category", "description"]
    top_operations_list = []
    counter = 0
    for row in sorted_operations_by_amount.loc[:, ["Дата операции",
                                                   "Сумма операции",
                                                   "Категория",
                                                   "Описание"]].iterrows():
        operation_dict = {}
        for i, element in enumerate(row[1]):
            operation_dict[fieldnames[i]] = element
        top_operations_list.append(operation_dict)
        counter += 1

        if counter == 5:
            break

    utils_logger.info("Конец работы функции get_top_transactions")
    return top_operations_list


def get_exchange_rates(currencies: list[str], base_currency='RUB') -> list[dict]:
    """
    Получение курсов валют по списку кодов
    """
    utils_logger.info("Начало работы функции get_exchange_rates")

    api_key_exchange_rates_data = os.getenv("API_KEY_EXCHANGE_RATES_DATA")
    headers = {"apikey": api_key_exchange_rates_data}
    currencies_list = []

    for currency in currencies:
        # Формируем URL
        url = (f"https://api.exchangeratesapi.io/v1/?access_key={api_key_exchange_rates_data}&from={currency}&to={base_currency}&amount=1")
        response = requests.get(url, headers=headers)

        # Проверяем статус ответа
        if response.status_code != 200:
            utils_logger.error(f"Ошибка при получении курса для {currency}: {response.text}")
            continue

        response_json = response.json()

        if "result" in response_json:
            currencies_list.append({
                "currency": currency,
                "rate": round(response_json["result"], 2)
            })
        else:
            utils_logger.warning(f"Ключ 'result' отсутствует в ответе API для {currency}: {response_json}")

    utils_logger.info("Конец работы функции get_exchange_rates")
    return currencies_list

def get_stock_rates(stock_list: list[str]) -> list[dict]:
    """
    Получение цен акций по списку кодов
    """
    utils_logger.info("Начало работы функции get_stock_rates")

    api_key_financial_modeling_prep = os.getenv("API_KEY_FINANCIAL_MODELING_PREP")
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key_financial_modeling_prep}"
    response = requests.get(url)
    stock_prices = []
    for share in response.json():
        stock_dict = {}
        if share["symbol"] in stock_list:
            stock_dict["stock"] = share["symbol"]
            stock_dict["price"] = round(share["price"], 2)
            stock_prices.append(stock_dict)

    utils_logger.info("Конец работы функции get_stock_rates")
    return stock_prices


def open_user_settings() -> Any:
    """
    Возвращает настройки из файла user_settings.json
    """
    utils_logger.info("Начало работы функции open_user_settings")

    with open("user_settings.json", "r") as file:
        result = json.load(file)

    utils_logger.info("Конец работы функции open_user_settings")
    return result
print(get_exchange_rates(["USD", "EUR"]))