import pandas as pd
import yfinance as yf

# Descargar los datos históricos de una acción (reemplaza 'AAPL' con el símbolo de la acción deseada)
ticker_symbol = 'WE'
data = yf.download(ticker_symbol, period='1y')

# Definir el tamaño de la ventana (window)
window_size = 30

# Crear una columna para la media ponderada
data['Media_Ponderada_Close'] = 0.0

# Calcular la media ponderada de Close utilizando una ventana de 30 días
for i in range(len(data) - window_size + 1):
    window_data = data.iloc[i:i + window_size]
    weighted_avg = (window_data['Close'] * window_data['Volume']).sum() / window_data['Volume'].sum()
    data.at[data.index[i + window_size - 1], 'Media_Ponderada_Close'] = weighted_avg

# Mostrar el DataFrame resultante con la columna de media ponderada
print(data[['Close', 'Volume', 'Media_Ponderada_Close']])
