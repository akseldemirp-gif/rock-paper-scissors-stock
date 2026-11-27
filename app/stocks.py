"""Load stock history for the command line and the web dashboard."""

import csv
import os
import re
from datetime import datetime
from math import isfinite
from pathlib import Path

import requests
from dotenv import load_dotenv

API_URL = "https://www.alphavantage.co/query"
SAMPLE_SYMBOLS = ("AAPL", "AMZN", "GOOG", "IBM", "MSFT")
SAMPLE_PATH = Path(__file__).with_name("data") / "stocks.csv"


class UnknownSymbol(ValueError):
    """No stock history is available for the requested ticker."""


class StockDataError(RuntimeError):
    """The upstream provider could not return usable stock data."""


def normalize_symbol(value):
    symbol = value.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,11}", symbol):
        raise UnknownSymbol("Enter a valid ticker symbol, such as AAPL or BRK.B.")
    return symbol


def sample_prices(symbol):
    if symbol not in SAMPLE_SYMBOLS:
        examples = ", ".join(SAMPLE_SYMBOLS)
        raise UnknownSymbol(f"No stock data found for {symbol}. Try {examples}.")
    with SAMPLE_PATH.open(newline="", encoding="utf-8") as file:
        return [
            {
                "date": datetime.strptime(row["date"], "%b %d %Y").date().isoformat(),
                "close": float(row["price"]),
            }
            for row in csv.DictReader(file)
            if row["symbol"] == symbol
        ]


def parse_daily_prices(payload, symbol):
    if not isinstance(payload, dict) or "Note" in payload or "Information" in payload:
        raise StockDataError("The stock data provider is temporarily unavailable. Try again later.")
    if "Error Message" in payload:
        raise UnknownSymbol(f"No stock data found for {symbol}. Check the ticker and try again.")

    series = payload.get("Time Series (Daily)")
    if not isinstance(series, dict) or not series:
        raise StockDataError("The stock data provider returned no daily prices. Try again later.")

    try:
        prices = [
            {
                "date": datetime.strptime(date, "%Y-%m-%d").date().isoformat(),
                "close": float(row["4. close"]),
            }
            for date, row in sorted(series.items())
        ]
    except (KeyError, TypeError, ValueError):
        raise StockDataError("The stock data provider returned invalid prices.") from None

    if any(not isfinite(row["close"]) or row["close"] <= 0 for row in prices):
        raise StockDataError("The stock data provider returned invalid prices.")
    return prices


def fetch_daily_prices(symbol, api_key):
    try:
        response = requests.get(
            API_URL,
            params={
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "outputsize": "compact",
                "apikey": api_key,
            },
            timeout=8,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        raise StockDataError("The stock data provider could not be reached. Try again later.") from None

    return parse_daily_prices(payload, symbol)


def get_stock_report(value, api_key=None):
    symbol = normalize_symbol(value)
    if api_key:
        prices = fetch_daily_prices(symbol, api_key)
        source = "Alpha Vantage · Daily close"
    else:
        prices = sample_prices(symbol)
        source = "Vega Datasets · Historical monthly prices"

    return {
        "symbol": symbol,
        "source": source,
        "currency": None if api_key else "USD",
        "prices": prices[-30:],
    }


if __name__ == "__main__":
    load_dotenv()
    try:
        report = get_stock_report(input("Stock ticker: "), os.getenv("ALPHAVANTAGE_API_KEY"))
    except (UnknownSymbol, StockDataError) as error:
        raise SystemExit(str(error)) from None

    print(f'{report["symbol"]} | {report["source"]}')
    for row in report["prices"]:
        print(f'{row["date"]}  {row["close"]:,.2f}')
