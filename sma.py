import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


desired_win = 1.06
stop_loss   = 0.9


desired_loss = 0.94
stop_short   = 1.1


def simulate_buy(price,data):
    for index, row in data.iterrows():
        if row["Low"]  < price*stop_loss :
            return row["Low"]/price
        if row["High"] > price* desired_win:
            return   desired_win

    last_row = data.iloc[-1]
    return last_row["Close"]/price


def simulate_sell(price,data):
    for index, row in data.iterrows():
        if row["High"]  > price*stop_short :
            return price/row["High"]
        if row["Low"] <  price* desired_loss:
            return   1.0/desired_loss
    try:
        last_row = data.iloc[-1]
        return last_row["Close"]/price
    except:
        return -1

# Definir el símbolo de la acción
ticker_symbol = "NVDA" 

# Calcular las fechas hace dos años y la fecha actual
end_date   = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=3650)).strftime('%Y-%m-%d')  

#En la variable va a quedar el histórico
data = yf.download(ticker_symbol, start=start_date)

long_sma = 40
short_sma = 10

days  = long_sma
sma_long_colname = 'SMA_' + str(days)
data[sma_long_colname] = data['Close'].rolling(window=days).mean()
delta_sma_long_colname = "d_"+sma_long_colname
data[delta_sma_long_colname] = ((data[sma_long_colname] - data[sma_long_colname].shift(1)) / data[sma_long_colname]) * 100

dias  = short_sma
sma_short_colname = 'SMA_' + str(dias)
delta_sma_short_colname = "d_"+sma_short_colname
data[sma_short_colname] = data['Close'].rolling(window=dias).mean()
data[delta_sma_short_colname] = ((data[sma_short_colname] - data[sma_short_colname].shift(1)) / data[sma_short_colname]) * 100
data = data.dropna()



data['Recomendacion'] = 'Esperar'  # Valor predeterminado de "Esperar"
data.loc[ (data[delta_sma_long_colname] > 0) & (data[delta_sma_short_colname] > 0), 'Recomendacion' ] = 'Compra'
data.loc[ (data[delta_sma_long_colname] < 0) & (data[delta_sma_short_colname] < 0), 'Recomendacion' ] = 'Venta'






future_window = 20
future_high =  'high_'+str(future_window) +'next'
future_low  =  'low_'+str(future_window) +'next'
data[future_high] =  data['High'].rolling(future_window).max().shift(-1*future_window)
data[future_low]  =  data['Low'].rolling(future_window).min().shift(-1*future_window)




data['Backtest'] = 'Esperar'      # Valor predeterminado de "Esperar"
data.loc[ (data[future_high] >= data["Close"]*desired_win) & (data[future_low]  >  data["Close"]*stop_loss), 'Backtest' ] = 'Compra'
data.loc[ (data[future_low]  < data["Close"]*desired_loss)  & (data[future_high] < data["Close"]*stop_short) ,'Backtest' ] = 'Venta'



data["simulate"] = 0
i = 0
num_rows = data.shape[0]
for index, row in data.iterrows():
    if (row["Recomendacion"] == "Compra"):
        data.at[index,"simulate"] =simulate_buy(row["Close"], data.tail(num_rows-i-1).head(100))
    if (row["Recomendacion"] == "Venta"):
        data.at[index,"simulate"] =simulate_sell(row["Close"], data.tail(num_rows-i-1).head(100))        
    i  = i+1


excel_filename = "DATA/"+ticker_symbol + "_historico_precios3.xlsx"
data.to_excel(excel_filename)

print(data)

data = data.tail(360)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data.index, data[sma_short_colname], label=sma_short_colname, linestyle='-', linewidth=1, color="blue")
ax.plot(data.index, data[sma_long_colname], label=sma_long_colname, linestyle='-', linewidth=2, color="orange")
ax.plot(data.index, data['Close'], label='Close', linestyle='-', linewidth=1, color="darkgray")




for index, row in data.iterrows():
    color = "gray"
    if row['Recomendacion'] == 'Compra':
        color = "green"
    if row['Recomendacion'] == 'Venta':        
        color = "red"    
    if color != "gray":        
        ax.plot(index, row['Close'], marker='o', markersize=4, color=color)

for index, row in data.iterrows():
    color = "gray"
    print("simulate",row['simulate'], type(row['simulate']))
    if row['simulate'] > 1 :
        print("GREEN")
        color = "green"

    if 0 < row['simulate'] and row['simulate'] < 1:
        print("ROJO")
        color = "red"        
    #if row['Backtest'] == 'Venta':        
    #    color = "red"    
    if color != "gray":        
        ax.plot(index, row['Close']*1.03, marker='+', markersize=7, color=color)



ax.set_title(f'Gráfico de SMA_{short_sma}, SMA_{long_sma} y Close para {ticker_symbol}')
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio')
ax.legend()

# Mostrar el gráfico
plt.grid(True)
plt.xticks(rotation=45)  # Rotar las fechas e n el eje x para que sean más legibles
plt.tight_layout()

plt.show()





