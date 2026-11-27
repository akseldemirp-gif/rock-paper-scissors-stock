"""Home, game, and stock-report routes."""

from random import choice

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app.rps import VALID_OPTIONS, determine_winner
from app.stocks import SAMPLE_SYMBOLS, StockDataError, UnknownSymbol, get_stock_report

home = Blueprint("home", __name__)
rps = Blueprint("rps", __name__, url_prefix="/rps")
stocks = Blueprint("stocks", __name__, url_prefix="/stocks")


@home.get("/")
@home.get("/home")
def index():
    return render_template("home.html")


@rps.get("/form")
def form():
    return render_template("rps_form.html", options=VALID_OPTIONS)


@rps.post("/play")
def play():
    player = request.form.get("choice", "")
    if player not in VALID_OPTIONS:
        flash("Choose rock, paper, or scissors to play.", "warning")
        return redirect(url_for("rps.form"), code=303)

    computer = choice(VALID_OPTIONS)
    result = determine_winner(player, computer)
    messages = {
        "USER WINS": "You win!",
        "COMPUTER WINS": "Computer wins.",
        "TIE GAME": "It's a tie.",
    }
    return render_template(
        "rps_result.html", player=player, computer=computer, result=messages[result]
    )


@stocks.get("/form")
def stock_form():
    return render_template(
        "stocks_form.html",
        samples=SAMPLE_SYMBOLS,
        historical=not current_app.config["ALPHAVANTAGE_API_KEY"],
    )


@stocks.post("/dashboard")
def dashboard():
    try:
        report = get_stock_report(
            request.form.get("symbol", ""), current_app.config["ALPHAVANTAGE_API_KEY"]
        )
    except (UnknownSymbol, StockDataError) as error:
        flash(str(error), "warning")
        return redirect(url_for("stocks.stock_form"), code=303)

    return render_template("stocks_dashboard.html", report=report)
