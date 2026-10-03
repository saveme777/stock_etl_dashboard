from pathlib import Path
from flask import Flask, render_template, request
import pandas as pd
from extract_and_load import extract_and_load

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    table_html = None  
    ticker = ""

    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip()
        
        if ticker:
            try:
                data = extract_and_load(ticker)
                table_html = data.tail(10).to_html(classes="stock-table", header=True, index=True)
            except ValueError as err:
                table_html = f"<p style='color: red;'>{err}</p>"

    return render_template("index.html", table=table_html, ticker=ticker)

if __name__ == '__main__':
    app.run(debug=True)