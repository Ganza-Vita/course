from unittest.mock import mock_open, patch
import pandas as pd
import os

from src.reports import out_to_json_file, out_to_user_file, spending_by_category


def test_spending_by_category(transactions_df: pd.DataFrame,
                              res_spending_by_category: pd.DataFrame) -> None:
    result = spending_by_category(transactions_df, "Супермаркеты", "2022.03.01")
    assert result.equals(res_spending_by_category)

def test_spending_by_category_without_date(transactions_df: pd.DataFrame,
                                           res_spending_by_category_without_date: pd.DataFrame) -> None:
    result = spending_by_category(transactions_df, "Супермаркеты")
    assert result.equals(res_spending_by_category_without_date)

def test_spending_by_category_empty(transactions_df: pd.DataFrame) -> None:
    result = spending_by_category(transactions_df, "Супермаркеты", "2025.03.01")
    assert result.empty

def test_out_to_json_file(transactions_df: pd.DataFrame) -> None:
    with patch('builtins.open', mock_open()) as mock_file:
        @out_to_json_file
        def example_1(transactions_df: pd.DataFrame) -> pd.DataFrame:
            return transactions_df

        result = example_1(transactions_df)
        assert result.equals(transactions_df)
        mock_file.assert_called_once_with("reports/report.json", "w")

def test_out_to_user_file(transactions_df: pd.DataFrame) -> None:
    with patch('builtins.open', mock_open()) as mock_file:
        @out_to_user_file("test.txt")
        def example_2(transactions_df: pd.DataFrame) -> pd.DataFrame:
            return transactions_df

        result = example_2(transactions_df)
        assert result.equals(transactions_df)
        mock_file.assert_called_once_with("reports/test.txt", "w")