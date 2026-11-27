from unittest.mock import Mock

import pytest

from app import stocks


def test_historical_report_has_sorted_prices():
    report = stocks.get_stock_report(" aapl ")
    assert report["symbol"] == "AAPL"
    assert len(report["prices"]) == 30
    dates = [row["date"] for row in report["prices"]]
    assert dates == sorted(dates)
    assert report["prices"][-1] == {"date": "2010-03-01", "close": 223.02}


@pytest.mark.parametrize("symbol", ["", "AAPL<script>", "NOTATICKER"])
def test_invalid_or_unknown_ticker(symbol):
    with pytest.raises(stocks.UnknownSymbol):
        stocks.get_stock_report(symbol)


def test_daily_prices_use_requested_ticker(monkeypatch):
    response = Mock()
    response.json.return_value = {
        "Time Series (Daily)": {
            "2026-02-05": {"4. close": "103.25"},
            "2026-02-04": {"4. close": "100.00"},
        }
    }
    get = Mock(return_value=response)
    monkeypatch.setattr(stocks.requests, "get", get)

    report = stocks.get_stock_report("BRK.B", api_key="test-key")

    assert get.call_args.kwargs["params"]["symbol"] == "BRK.B"
    assert report["prices"] == [
        {"date": "2026-02-04", "close": 100.00},
        {"date": "2026-02-05", "close": 103.25},
    ]
