import datetime
import json
import logging
import os.path
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

import os
import logging

# Создаем директорию logs, если ее нет
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)  # создает папку, если её нет

reports_file_handler = logging.FileHandler(f"{log_directory}/{__name__}.log", "w")
logging.basicConfig(
    handlers=[reports_file_handler],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def out_to_json_file(func: Callable) -> Callable:
    """
    Запись датафрейма в файл records.json в JSON формате
    """

    @wraps(func)
    def wrapper(*args: list, **kwargs: list) -> Any:
        result = func(*args, **kwargs)

        reports_logger.info("Выгрузка отчета в файл report.json")
        wrapper_result = result.to_dict("records")
        wrapper_result = json.dumps(wrapper_result, indent=4, ensure_ascii=False)
        with open("reports/report.json", "w") as file:
            file.write(wrapper_result)
        return result

    return wrapper


def out_to_user_file(file_name: str) -> Callable:
    """
    Запись датафрейма в пользовательский файл в CSV формате
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: list, **kwargs: list) -> Any:
            result = func(*args, **kwargs)
            reports_logger.info(f"Выгрузка отчета в файл {file_name}")
            wrapper_result = result.to_csv()
            with open(os.path.join("reports/", file_name), "w") as file:
                file.write(wrapper_result)
            return result

        return wrapper

    return decorator


@out_to_user_file(file_name="spending_by_category.txt")
@out_to_json_file
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ Опицонально принимает дату в формате ГГГГ.ММ.ДД"""
    reports_logger.info("Начало формирования отчета")
    reports_logger.info("Определение конечной даты")
    if date:
        end_date = datetime.datetime.strptime(date, "%Y.%m.%d")
    else:
        end_date = datetime.datetime.now()

    reports_logger.info("Определение начальной даты")
    if end_date.month <= 3:
        start_date = end_date.replace(year=end_date.year - 1, month=end_date.month + 12 - 3)
    else:
        start_date = end_date.replace(month=end_date.month - 3)

    reports_logger.info("Фильтрация данных по дате")
    df_date = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    transactions = transactions[(start_date <= df_date) & (df_date <= end_date)]

    reports_logger.info("Фильтрация данных по категории")
    transactions = transactions[transactions["Категория"] == category]
    expenses = pd.DataFrame(transactions[transactions["Сумма операции"] < 0])
    reports_logger.info("Конец формирования отчета")
    return expenses
