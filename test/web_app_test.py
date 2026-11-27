import pytest

from web_app import create_app


@pytest.fixture
def client():
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test-key",
        "ALPHAVANTAGE_API_KEY": "",
        "SESSION_COOKIE_SECURE": False,
    }).test_client()


@pytest.mark.parametrize("path", ["/", "/home"])
def test_home_routes(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert b"<h1>Rock, Paper, Scissors, Stock!</h1>" in response.data


def test_rps_form_and_result(client, monkeypatch):
    assert b'<option value="scissors">' in client.get("/rps/form").data
    monkeypatch.setattr("web_app.routes.choice", lambda options: "scissors")
    response = client.post("/rps/play", data={"choice": "rock"})
    assert response.status_code == 200
    assert b"You win!" in response.data
    assert b"<dd>Rock</dd>" in response.data
    assert b"<dd>Scissors</dd>" in response.data


def test_stock_form_and_dashboard(client):
    assert b'<input id="symbol"' in client.get("/stocks/form").data
    response = client.post("/stocks/dashboard", data={"symbol": "aapl"})
    assert response.status_code == 200
    assert b"AAPL price history" in response.data
    assert b"<table" in response.data and b"<td>2010-03-01</td>" in response.data
    assert b'<canvas id="price-chart"' in response.data and b'"close": 223.02' in response.data


def test_invalid_ticker_redirects_and_flashes(client):
    response = client.post("/stocks/dashboard", data={"symbol": "NOTATICKER"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/stocks/form"
    assert b'role="alert"' in response.data
    assert b"No stock data found for NOTATICKER" in response.data
