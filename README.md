# Rock, Paper, Scissors, Stock!

A Flask web app for playing Rock Paper Scissors and charting stock prices. The web pages and command-line programs share the same game rules and stock-report code.

## Run locally

Requires Python 3.11 or later.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app web_app run
```

Open [localhost:5000](http://localhost:5000). The game is at `/rps/form` and the stock lookup is at `/stocks/form`. For the command-line versions, run `python -m app.rps` or `python -m app.stocks`.

## Stock data

The default lookup uses monthly prices from the [Vega Datasets stocks sample](https://vega.github.io/vega-datasets/datasets/stocks/). It supports AAPL, AMZN, GOOG, IBM, and MSFT with data from 2000–2010. The chart and table show up to 30 observations.

To look up current daily history and other tickers, copy `.env.example` to `.env` and set `ALPHAVANTAGE_API_KEY` with an [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key). The dashboard then uses Alpha Vantage daily closing prices. On Render, set the same variable in the service's Environment page.

## Tests and deployment

Run `python -m pytest` from the repository root. GitHub Actions runs tests for pushes and pull requests to `main`. The tests use local stock data and mocked provider responses, so they require no API key.

See [DEPLOYING.md](DEPLOYING.md) for the Render setup.
