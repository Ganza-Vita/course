from typing import Any
from unittest.mock import patch

import pandas as pd

import src.views


@patch("src.views.get_exchange_rates")
@patch("src.views.get_stock_rates")
@patch("src.views.open_user_settings")
@patch("src.views.get_data_filter_by_date")
def test_main(mock_data: Any, mock_settings: Any, mock_stock: Any, mock_exchange: Any,
              res_main: str, res_get_data_filter_by_date: pd.DataFrame) -> None:
    mock_data.return_value = res_get_data_filter_by_date
    mock_settings.return_value = {"user_currencies": ["USER"],
                                  "user_stocks": ["USER"]}
    mock_stock.return_value = [{'stock': 'USER', 'price': 100}]
    mock_exchange.return_value = [{'currency': 'USER', 'rate': 100}]
    assert src.views.main("2021-12-31 16:44:00") == res_main