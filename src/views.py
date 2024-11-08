import datetime
import json
import logging

from src.utils import (get_cards_info, get_data_filter_by_date, get_exchange_rates, get_stock_rates,
                       get_top_transactions, greetings, open_user_settings)

views_logger = logging.getLogger(__name__)
views_file_formater = logging.Formatter(
    "%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
    "%d.%m.%Y %H:%M:%S")
views_file_handler = logging.FileHandler("logs/project.log", "a")
views_file_handler.setFormatter(views_file_formater)
views_logger.setLevel(logging.DEBUG)
views_logger.addHandler(views_file_handler)


def main(user_date: str) -> str:
    """
    Функция принимает строку с датой  и временем в формате YYYY-MM-DD HH:MM:SS и возвращает JSON-ответ
    """
    views_logger.info("Начало работы")
    end_date = datetime.datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")

    views_logger.info("Приветствие")
    greeting = greetings(end_date)

    views_logger.info("Получение данных")
    operations = get_data_filter_by_date("operations.xlsx", end_date)

    views_logger.info("Получение статистики по картам")
    cards_list = get_cards_info(operations)

    views_logger.info("Получение топ транзаций")
    top_operations_list = get_top_transactions(operations)

    views_logger.info("Получение пользовательских настроек")
    user_settings = open_user_settings()

    views_logger.info("Получение данных курса валют")
    currencies_list = get_exchange_rates(user_settings["user_currencies"])

    views_logger.info("Получение данных курса акций")
    stock_prices = get_stock_rates(user_settings["user_stocks"])

    result_dict = {"greeting": greeting,
                   "cards": cards_list,
                   "top_transactions": top_operations_list,
                   "currency_rates": currencies_list,
                   "stock_prices": stock_prices}

    views_logger.info("Конец работы")
    return json.dumps(result_dict, ensure_ascii=False)