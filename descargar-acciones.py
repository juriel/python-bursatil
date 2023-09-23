import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

stock_symbols = ["PFGRUPSURA.CL","AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

excel_writer = pd.ExcelWriter("stock_price_history.xlsx", engine="openpyxl")

end_date   = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=730)).strftime('%Y-%m-%d')

print(" Fechas ",start_date, end_date)

for symbol in stock_symbols:
    print("Vamos a descargar historico de ",symbol)
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    stock_data.to_excel(excel_writer, sheet_name=symbol)

excel_writer.save()



