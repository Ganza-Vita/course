import pandas as pd

from src.services import increase_cashback


def test_increase_cashback_12(transactions_df: pd.DataFrame, cashback_12: str) -> None:
    result = increase_cashback(transactions_df, 2021, 12)
    assert result == cashback_12


 def test_increase_cashback(transactions_df: pd.DataFrame) -> None:
    result = increase_cashback(transactions_df, 2024, 7)
    assert result == """"{"Супермаркеты": 50}"""