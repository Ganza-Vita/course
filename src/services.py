import datetime
import json
import logging

import pandas as pd

services_logger = logging.getLogger(__name__)
services_file_formater = logging.Formatter(
    "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
    "%d.%m.%Y %H:%M:%S")
services_file_handler = logging.FileHandler(f"logs/{__name__}.log", "w")
services_file_handler.setFormatter(services_file_formater)
services_logger.setLevel(logging.DEBUG)
services_logger.addHandler(services_file_handler)


def increase_cashback(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Функция анализирует наиболее выгодные категории кэшбэка в переданном датафрэйме
    """
    services_logger.info("Начало работы сервиса")
    services_logger.info("Определение начальной даты")
    start_date = datetime.datetime(year=year, month=month, day=1)
    if month == 12:
        end_date = start_date.replace(year=year + 1, month=1) - datetime.timedelta(seconds=1)
    else:
        end_date = start_date.replace(month=month + 1) - datetime.timedelta(seconds=1)

    services_logger.info("Фильтрация данных по дате и выплате кэшбэка")
    df_date = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    data = data[(start_date <= df_date) & (df_date <= end_date)]
    cashback = data[data["Кэшбэк"] > 0]

    services_logger.info("Группировка данных по категориям")
    data_group_category = cashback.groupby("Категория").agg({"Кэшбэк": "sum"})
    data_group_category.sort_values(by="Кэшбэк", ascending=False, inplace=True)

    services_logger.info("Конвертация данных")
    result_dict = data_group_category.to_dict(orient="dict")
    result = json.dumps(result_dict["Кэшбэк"], ensure_ascii=False)

    services_logger.info("Конец работы сервиса")
    return result
