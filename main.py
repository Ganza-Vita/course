import os
import pandas as pd
import logging
from src.reports import spending_by_category
from src.services import increase_cashback
from src.views import main

# Установка конфигурации логирования
logging.basicConfig(level=logging.INFO)

def main_program():
    data_file_path = "data/operations.xlsx"

    if not os.path.exists(data_file_path):
        logging.error(f"Файл {data_file_path} не найден.")
        return

    try:
        data = pd.read_excel(data_file_path)
    except Exception as e:
        logging.error(f"Ошибка при чтении данных из Excel: {e}")
        return

    try:
        cashback_result = increase_cashback(data, 2021, 11)
        spending_result = spending_by_category(data, "Супермаркеты", "2022-03-01")
        logging.info(f"Кэшбэк: {cashback_result}")
        logging.info(f"Расходы по категориям: {spending_result}")
    except Exception as e:
        logging.error(f"Ошибка при обработке данных: {e}")

if __name__ == "__main__":
    print(main("2021-12-31 16:44:00"))
    main_program()