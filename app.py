from pathlib import Path

from flask import Flask, render_template, request
import pandas as pd

from extract_and_load import extract_and_load

app = Flask(__name__)

@app.route('/')
def index():
    ticker = "AAPL"
    file_path = Path(__file__).resolve().parent / f"{ticker}_transformed.csv"
    if file_path.exists():
        data = pd.read_csv(file_path, index_col=0)
        if data.index[:3].tolist() == ["Price", "Ticker", "Date"]:
            data = pd.read_csv(file_path, index_col=0, header=[0, 1, 2])
            data.columns = data.columns.get_level_values(0)
        table_html = data.tail(10).to_html(
            classes="stock-table", header=True, index=True
        )
    else:
        table_html = "<p style='color: red;'>Файл данных не найден! Сначала введи тикер.</p>"

    return render_template("index.html", table=table_html, ticker=ticker)


@app.route("/", methods=["POST"])
def submit_ticker():
    ticker = request.form.get("ticker", "").strip().upper()
    try:
        data = extract_and_load(ticker)
        table_html = data.tail(10).to_html(
            classes="stock-table", header=True, index=True
        )
        error = None
    except ValueError as exc:
        table_html = ""
        error = str(exc)

    return render_template(
        "index.html", table=table_html, ticker=ticker, error=error
    )

if __name__ == '__main__':
    app.run(debug=True)