from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    file_name = "AAPL_transformed.csv"
    
    try:
        data = pd.read_csv(file_name, index_col=0)
    
        table_html = data.tail(10).to_html(classes='stock-table', header=True, index=True)
        
    except FileNotFoundError:
        table_html = "<p style='color: red;'>Файл данных не найден! Сначала запусти ETL-скрипт.</p>"
        
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run(debug=True)